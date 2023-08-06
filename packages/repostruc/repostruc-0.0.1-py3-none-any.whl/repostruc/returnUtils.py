from pathlib import Path
import pyperclip

class ReturnHandler():   
    """
    ReturnHandler contains methods to return the Directory tree :
    
    @functions
    copyToClipboard     => Copies tree structure to clipboard.
    saveAsFile          => Saves tree structure to a file.
    
    """

    headDoc ="""
# Product Name

> Short blurb about what your product does.

## File Structure

```markdown
"""
    tailDoc ="""

```

## Contributing

1. Fork it (<https://github.com/yourname/yourproject/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request
"""

    @staticmethod
    def copyToClipboard(tree_contents: list):
        """
        Saves Tree contents to clipboard.
        @param tree_contents: List object containing tree contents.
        """
        text = '\n'.join(map(str, tree_contents))
        pyperclip.copy(text)

    @staticmethod
    def saveAsFile(tree_contents: list, file_path: Path, readme: bool=False):
        """
        Saves Tree contents to file or readme.
        @param tree_contents: List object containing tree contents.
        @param file_path: Path to the file
        @param readme: True if file is readme
        """
        text = '\n'.join(map(str, tree_contents))
        if readme:
            with open(file_path, 'w', encoding="utf-8") as f:
                f.write(ReturnHandler.headDoc)
                f.write(text)
                f.write(ReturnHandler.tailDoc)
        else:
            with open(file_path, 'w', encoding="utf-8") as f:
                f.write(text)
