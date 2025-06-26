#tests for our Get_Files_Info function

from functions.get_files_info import get_files_info as get_info
from functions.get_file_content import get_file_content as get_file
from functions.write_file import write_file as write_file
from functions.run_python_file import run_python_file as run_python_file

def main():
    # Tests for Get_Files_Info function
    """
    print("test1 test1 test1 test1")
    print(get_info("calculator", "."))

    print("\n test2 test2 test2 test2 \n")
    print(get_info("calculator", "pkg"))

    print("\n **********test3 test3 test3 test3********** \n")
    print(get_info("calculator", "/bin"))

    print("\n **********test4 test4 test4 test4********* \n")
    print(get_info("calculator", "../"))    
    """

    # tests for Get_File_Content
    """
    print("===============TEST1===============")
    #print(get_file("calculator", "lorem.txt"))
    print(get_file("calculator", "main.py"))

    print("\n==================TEST2=================")
    print(get_file("calculator", "pkg/calculator.py"))

    print("\n======================TEST3====================")
    print(get_file("calculator", "/bin/cat"))
    """

    #tests for Write_File
    """
    print("===============TEST1=============")
    print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))

    print("\n==================TEST2============")
    print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))

    print("\n================TEST3==============")
    print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"))
    """

    # tests for Run_Python_File
    print(run_python_file("calculator", "main.py") + "\n\n")
    print(run_python_file("calculator", "tests.py") + "\n\n")
    print(run_python_file("calculator", "../main.py") + "\n\n")
    print(run_python_file("calculator", "nonexistent.py"))


if __name__ == "__main__":
    main()