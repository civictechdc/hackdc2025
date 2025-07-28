class WriteOnceDict(dict):
    """
    A dictionary subclass that allows access to keys using dot notation
    and prevents keys from being overwritten or deleted once they are set.

    This is a low level class and needs no dependancies

    Attributes:
        _locked_keys (set): A set of keys that cannot be modified or deleted once set.
    """
    
    def __init__(self, *args, **kwargs):
        """
        Initializes the WriteOnceDict with optional key-value pairs.

        Args:
            *args: Variable length argument list for initial key-value pairs.
            **kwargs: Arbitrary keyword arguments for initial key-value pairs.
        """
        super(WriteOnceDict, self).__init__(*args, **kwargs)
        # Directly setting the attribute without triggering __setattr__
        super().__setattr__('_locked_keys', set(self.keys()))

    def __getattr__(self, name):
        """
        Allows access to dictionary keys using dot notation.
        
        Args:
            name (str): The name of the attribute/key to access.
        
        Returns:
            The value associated with the key.
        
        Raises:
            AttributeError: If the key does not exist.
        """
        try:
            return self[name]
        except KeyError:
            raise AttributeError(f"WriteOnceDict Error: object has no attribute '{name}'")

    def __setattr__(self, name, value):
        """
        Sets the value for a key using dot notation. Prevents overwriting existing keys.
        
        Args:
            name (str): The name of the attribute/key to set.
            value: The value to associate with the key.
        
        Raises:
            KeyError: If attempting to overwrite an existing key.
        """
        if hasattr(self, '_locked_keys') and name in self._locked_keys:
            raise KeyError(f"WriteOnceDict Error: Cannot overwrite existing key: '{name}'")
        self[name] = value
        if hasattr(self, '_locked_keys'):
            self._locked_keys.add(name)

    def __setitem__(self, key, value):
        """
        Sets the value for a key using dictionary syntax. Prevents overwriting existing keys.
        
        Args:
            key: The key to set.
            value: The value to associate with the key.
        
        Raises:
            KeyError: If attempting to overwrite an existing key.
        """
        if key in self._locked_keys:
            raise KeyError(f"WriteOnceDict Error: Cannot overwrite existing key: '{key}'")
        super(WriteOnceDict, self).__setitem__(key, value)
        self._locked_keys.add(key)

    def __delattr__(self, name):
        """
        Prevents deletion of attributes using dot notation.
        
        Args:
            name (str): The name of the attribute/key to delete.
        
        Raises:
            AttributeError: Always, as deletion is not allowed.
        """
        raise AttributeError("WriteOnceDict Error: Cannot delete attributes from a WriteOnceDict")

    def __delitem__(self, key):
        """
        Prevents deletion of keys using dictionary syntax.
        
        Args:
            key: The key to delete.
        
        Raises:
            KeyError: Always, as deletion is not allowed.
        """
        raise KeyError("WriteOnceDict Error: Cannot delete keys from a WriteOnceDict")



