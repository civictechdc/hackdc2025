

--
-- Table structure for table `comment`
--

CREATE TABLE `comment` (
  `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  `commentId` varchar(100) NOT NULL UNIQUE,
  `comment_on_documentId` varchar(50) NOT NULL,
  `comment_date_text` varchar(50) NOT NULL,
  `comment_date` datetime DEFAULT NULL,
  `comment_text` longtext NOT NULL
);

-- --------------------------------------------------------

--
-- Table structure for table `comment_full`
--

CREATE TABLE `comment_full`(
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `commentId` varchar(100) NOT NULL UNIQUE,
  `comment_on_documentId` varchar(50) NOT NULL,
  `comment_date_text` varchar(50) NOT NULL,
  `comment_date` datetime DEFAULT NULL,
  `comment_text` longtext NOT NULL
);

-- --------------------------------------------------------

--
-- Table structure for table `llm_reply_per_comment`
--

CREATE TABLE `llm_reply_per_comment` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `question_id` int(11) NOT NULL UNIQUE,
  `answer` varchar(1000) NOT NULL,
  `commentId` varchar(100) NOT NULL,
  `chatbot_id` int(11) NOT NULL DEFAULT 1,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- --------------------------------------------------------

--
-- Table structure for table `questions_for_llm`
--

CREATE TABLE `questions_for_llm` (
  `id` INTEGER PRIMARY KEY,
  `question_text` varchar(1000) NOT NULL
);

