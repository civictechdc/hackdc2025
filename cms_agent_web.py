#!/usr/bin/env python3

import streamlit as st
import boto3
import json
import dotenv
from typing import List, Dict, Any
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
dotenv.load_dotenv()

class CMSAgent:
    def __init__(self):
        """Initialize the CMS Agent with AWS clients."""
        # Create Bedrock Runtime and S3 Vectors clients
        self.bedrock = boto3.client("bedrock-runtime", region_name='us-east-1')
        self.s3vectors = boto3.client("s3vectors", region_name='us-east-1')
        self.vector_bucket_name = "ekim-civictech-hackathon-2025"
        self.vector_index_name = "cms-titan-3"
        self.max_retrieval_rounds = 3  # Maximum number of retrieval rounds
        
    def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for input text using Amazon Titan Text Embeddings V2."""
        # Truncate text if it's too long (Titan has a context limit)
        if len(text) > 8000:
            text = text[:8000]
            
        response = self.bedrock.invoke_model(
            modelId="amazon.titan-embed-text-v2:0",
            body=json.dumps({"inputText": text})
        )

        # Extract embedding from response
        response_body = json.loads(response["body"].read())
        return response_body["embedding"]
    
    def query_vector_store(self, query: str, top_k: int = 5) -> List[Dict[Any, Any]]:
        """Query the vector store with the given query text."""
        # logger.info(f"Querying vector store with query: {query}")
        # Generate embedding for the query
        query_embedding = self.generate_embedding(query)
        
        # Query vector index
        response = self.s3vectors.query_vectors(
            vectorBucketName=self.vector_bucket_name,
            indexName=self.vector_index_name,
            queryVector={"float32": query_embedding}, 
            topK=top_k, 
            returnDistance=True,
            returnMetadata=True
        )
        # logger.info(f"Response from vector store: {response}")
        return response["vectors"]

    def generate_response(self, query: str, top_k: int = 5) -> Dict[str, Any]:
        """Generate a response to the user's query about CMS dockets with agentic retrieval."""
        # Initial retrieval round
        results = self.query_vector_store(query, top_k=top_k)
        contexts, sources = self._extract_context_and_sources(results)
        
        # First attempt at answering
        prompt = self._create_prompt(query, contexts, is_follow_up=False)
        answer, needs_more_info = self._get_model_response(prompt)
        
        # Agentic retrieval loop - get more context if needed
        retrieval_round = 1
        while needs_more_info and retrieval_round < self.max_retrieval_rounds:
            logger.info(f"Retrieval round {retrieval_round+1}: Model needs more information")
            
            # Generate a refined query based on what's missing
            refine_prompt = self._create_refine_query_prompt(query, answer, contexts)
            refined_query = self._get_refined_query(refine_prompt)
            
            # Get additional context with the refined query
            additional_results = self.query_vector_store(refined_query, top_k=top_k)
            additional_contexts, additional_sources = self._extract_context_and_sources(additional_results)
            
            # Add new unique contexts and sources
            for context in additional_contexts:
                if context not in contexts:
                    contexts.append(context)
            
            for source in additional_sources:
                if source not in sources:
                    sources.append(source)
            
            # Try answering again with expanded context
            prompt = self._create_prompt(query, contexts, is_follow_up=True)
            answer, needs_more_info = self._get_model_response(prompt)
            
            retrieval_round += 1
        
        return {
            "query": query,
            "answer": answer,
            "sources": sources
        }
    
    def _extract_context_and_sources(self, results):
        """Extract context and source information from vector search results."""
        contexts = []
        sources = []
        
        for result in results:
            logger.info(f"Result: {result}")
            if "metadata" in result and "source_text" in result["metadata"]:
                contexts.append(result["metadata"]["source_text"])
                
                # Extract source information
                source_info = {}
                if "docket_id" in result["metadata"]:
                    source_info["docket_id"] = result["metadata"]["docket_id"]
                if "comment_id" in result["metadata"]:
                    source_info["comment_id"] = result["metadata"]["comment_id"]    
                if "link" in result["metadata"]:
                    source_info["link"] = result["metadata"]["link"]                                
                if "title" in result["metadata"]:
                    source_info["title"] = result["metadata"]["title"]
                if "document_type" in result["metadata"]:
                    source_info["document_type"] = result["metadata"]["document_type"]
                if "posted_date" in result["metadata"]:
                    source_info["posted_date"] = result["metadata"]["posted_date"]
                logger.info(f"Source info: {source_info}")
                sources.append(source_info)
                
        return contexts, sources
    
    def _get_model_response(self, prompt: str) -> tuple:
        """Get response from the LLM and determine if more information is needed."""
        response = self.bedrock.invoke_model(
            modelId="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
            body=json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 1000,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            })
        )
        
        response_body = json.loads(response["body"].read())
        answer = response_body["content"][0]["text"]
        
        # Check if the answer indicates more information is needed
        needs_more_info = self._needs_more_information(answer)
        
        return answer, needs_more_info
    
    def _needs_more_information(self, answer: str) -> bool:
        """Determine if the answer indicates more information is needed."""
        # Check for phrases indicating incomplete information
        indicators = [
            "don't have enough information",
            "insufficient information",
            "not enough context",
            "can't determine",
            "need more details",
            "information is limited",
            "context doesn't provide",
            "can't answer fully",
            "limited context"
        ]
        
        return any(indicator.lower() in answer.lower() for indicator in indicators)
    
    def _create_refine_query_prompt(self, original_query: str, current_answer: str, current_contexts: List[str]) -> str:
        """Create a prompt to generate a refined search query."""
        context_summary = "\n\n".join(current_contexts[:3])  # Use first few contexts for brevity
        
        prompt = f"""Based on the original user question and the current answer, generate a new search query that would help retrieve additional relevant information.

        ORIGINAL QUESTION: {original_query}
        
        CURRENT ANSWER: {current_answer}
        
        CURRENT CONTEXT SUMMARY (partial):
        {context_summary}
        
        Your task is to create a new search query that will help find additional information to better answer the original question. Focus on aspects that seem to be missing or incomplete in the current answer.
        
        Return ONLY the new search query text, nothing else.
        """
        return prompt
    
    def _get_refined_query(self, prompt: str) -> str:
        """Get a refined query from the LLM."""
        response = self.bedrock.invoke_model(
            modelId="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
            body=json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 100,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            })
        )
        
        response_body = json.loads(response["body"].read())
        refined_query = response_body["content"][0]["text"].strip()
        logger.info(f"Refined query: {refined_query}")
        
        return refined_query
    
    def _create_prompt(self, query: str, contexts: List[str], is_follow_up: bool = False) -> str:
        """Create a prompt for the LLM using the query and retrieved contexts."""
        context_text = "\n\n".join(contexts)
        
        # Adjust prompt based on whether this is an initial or follow-up query
        if not is_follow_up:
            prompt = f"""You are a helpful assistant that answers questions about CMS (Centers for Medicare & Medicaid Services) dockets, regulations, Medicare, and Medicaid programs.
            
            Below is information retrieved from CMS documents that may help answer the user's question.

            RETRIEVED CONTEXT:
            {context_text}

            USER QUESTION: {query}

            Please answer the question based on the retrieved context. Be particularly thorough when addressing questions about:
            - Common issues with Medicare
            - Changes to Medicaid eligibility
            - Recent CMS final rules and their key points
            - CMS regulation of telehealth services
            - Medicare and Medicaid coverage policies

            If the context doesn't contain enough information to answer the question fully, acknowledge what you know and what you don't know. Be specific about what additional information would be helpful. Use phrases like "I don't have enough information about X" or "The context doesn't provide details on Y."

            If the question is about Medicare or Medicaid but the context doesn't provide sufficient information, you can still provide general information about these programs while noting that your answer isn't based on the most recent regulations.

            If the question is not related to CMS dockets, regulations, Medicare, or Medicaid, politely explain that you're focused on helping with CMS-related inquiries.
            """
        else:
            prompt = f"""You are a helpful assistant that answers questions about CMS (Centers for Medicare & Medicaid Services) dockets, regulations, Medicare, and Medicaid programs.
            
            Below is expanded information retrieved from CMS documents that may help answer the user's question. This includes additional context that was retrieved to provide a more complete answer.

            EXPANDED RETRIEVED CONTEXT:
            {context_text}

            USER QUESTION: {query}

            Please provide a comprehensive answer to the question based on all the retrieved context. Be particularly thorough and try to address all aspects of the question.

            If there are still aspects of the question that cannot be answered with the available information, acknowledge this clearly.
            """
        
        return prompt


# Streamlit UI
def main():
    st.set_page_config(
        page_title="CMS Docket Assistant",
        page_icon="🏥",
        layout="wide"
    )
    
    # Initialize the agent
    if 'agent' not in st.session_state:
        st.session_state.agent = CMSAgent()
    
    # Initialize chat history
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    # Header
    st.title("CMS Docket Assistant")
    st.markdown("""
    Ask questions about CMS (Centers for Medicare & Medicaid Services) dockets and regulations.
    This assistant uses AI to search through CMS documents and provide relevant information.
    """)
    
    # Sidebar with information
    with st.sidebar:
        st.header("About")
        st.markdown("""
        This assistant helps you find information about CMS dockets and regulations.
        
        It uses:
        - Vector embeddings to search through CMS documents
        - Amazon Bedrock for AI processing
        - Streamlit for the web interface
        
        **Example questions:**
        - What are common issues with Medicare?
        - Explain the latest changes to Medicaid eligibility
        - What are the key points in the recent CMS final rule?
        - How does CMS regulate telehealth services?
        """)
        
        st.header("Settings")
        top_k = st.slider("Number of sources to retrieve", min_value=1, max_value=10, value=5)
        
        # Add clear chat button
        if st.button("Clear Chat"):
            st.session_state.messages = []
            st.rerun()
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
            # If this is an assistant message with sources, display them in an expander
            if message["role"] == "assistant" and "sources" in message:
                with st.expander("View Sources"):
                    for i, source in enumerate(message["sources"], 1):
                        st.markdown(f"**Source {i}**")
                        st.markdown(f"**Title:** {source.get('title', 'Untitled')}")
                        st.markdown(f"**Docket ID:** {source.get('docket_id', 'No docket ID')}")
                        st.markdown(f"**Comment ID:** {source.get('comment_id', 'No comment ID')}")
                        st.markdown(f"**Link:** https://www.regulations.gov/comment/{source.get('comment_id', 'No link')}")
                        if "document_type" in source:
                            st.markdown(f"**Document Type:** {source['document_type']}")
                        if "posted_date" in source:
                            st.markdown(f"**Posted Date:** {source['posted_date']}")
                        st.divider()
    
    # User input
    if prompt := st.chat_input("Ask a question about CMS dockets and regulations"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Display assistant response with a spinner while processing
        with st.chat_message("assistant"):
            with st.spinner("Searching CMS documents..."):
                try:
                    # Generate response
                    result = st.session_state.agent.generate_response(prompt, top_k=top_k)
                    
                    # Display the answer
                    st.markdown(result["answer"])
                    
                    # Store sources for display in expander
                    sources = result["sources"]
                    
                    # Add assistant message to chat history
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": result["answer"],
                        "sources": sources
                    })
                    
                    # Display sources in an expander
                    with st.expander("View Sources"):
                        for i, source in enumerate(sources, 1):
                            st.markdown(f"**Source {i}**")
                            st.markdown(f"**Title:** {source.get('title', 'Untitled')}")
                            st.markdown(f"**Docket ID:** {source.get('docket_id', 'No docket ID')}")
                            st.markdown(f"**Comment ID:** {source.get('comment_id', 'No comment ID')}")
                            st.markdown(f"**Link:** https://www.regulations.gov/comment/{source.get('comment_id', 'No link')}")
                            if "document_type" in source:
                                st.markdown(f"**Document Type:** {source['document_type']}")
                            if "posted_date" in source:
                                st.markdown(f"**Posted Date:** {source['posted_date']}")
                            st.divider()
                            
                except Exception as e:
                    error_msg = f"Error: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})


if __name__ == "__main__":
    main() 