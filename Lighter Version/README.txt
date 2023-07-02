

I have used LCS along with edit-distance to detect plagiarism between two given files. My approach for this project is stated below,

Step 1: Read both files.

    Here, I retrieve the paths of files using command line arguments and read both files using Python’s standard library. This returns a string of file content as output.


Step 2: Check both files, whether they are text files or code files.

First, I created a list of words from the file-string obtained in step 1 and compared it with a list of keywords for various programming languages such as Python, Java, and C++.Based on this comparison, if at least 25.50% of the words in a file match with language keywords, then I declare that file as a Code File or else a Text File.


Step 3: If both files do not belong to the same class, then return 0.

    For example, after step-2, if file1.txt is a code file and file2.txt is a text file, or vice versa, then I return 0, as there should not be any plagiarism between two different classes of files, which is obvious.


Step 4: If both are text files, then apply the strategy to detect plagiarism for Text Files.

    To detect plagiarism between two text files, first I prepare two lists for both files,
        (i)     a bag(list) of words for the whole file, let’s call it "All-Word-List"
        (ii)    a bag(list) of words related to reference link mentioned inside that file, let’s call it"Ref-Word-List"

    Then I compare Ref-Word-List with All-Word-List and remove similar as well as nearest word to the ref-word from All-Word-List. Here, I use normal LCS and Edit-Distance strategies to decide the closeness of ref-Word to All-Word.
    
    Once reference-related words are removed from both file lists, I simply apply word-to-word LCS in the same sequence as they are written in the text file to check the similarity between the two files.
    
    At last, I calculate average percentage match based on LCS with respect to both file size and return 0 if matching ratio is lesser then 40% or else 1.


Step 5: If both are code files, then apply the strategy to detect plagiarism for Code Files.

    In Code files, we do not have to check for any references. Thus, I prepare All-Word-List for both the files and then apply word-to-word LCS compare between both file's All-Word-List which is same as step-4.

    Again, based on the average matching percentage retrieved from the above word-to-word LCS, I decide whether plagiarism is detected or not. If match at least 40% then I return 1 or else 0.
