import unittest  
from glob import glob  
import os  
from solver import TileReplacementSolver  # Importing the solver class to solve the tile replacement problem

class TileReplacementUnitTest(unittest.TestCase):
    test_directory = r'./input'  # Directory containing the input test files
    test_file_type = r'*.txt'  # File extension pattern for the input files (only .txt files)

    def test_cases(self) -> None:
        """
        This method will iterate over all input files in the specified directory
        and run the tile replacement solver on each of them.
        It will check if the number of target tiles matched is correct.
        """

        # Iterate over all files in the test directory that match the given file type
        for filepath in glob(
            os.path.join(self.test_directory, self.test_file_type)  # Combine directory and file pattern to match
        ):
            print(f'Processing {filepath} ...')  # Log the current file being processed
            solver = TileReplacementSolver(filepath)  # Initialize the solver with the current file
            solver.solve()  # Solve the tile replacement problem

            # Check if the solver was able to solve the problem
            if solver.is_solved:
                # If solved, attempt to apply the solution to the landscape
                for x, y, tile in solver.path:
                    solver.put_tile(tile, solver.landscape, x, y)  # Place the tile on the landscape at the specified coordinates

                # Count occurrences of each tile type in the landscape
                digits = solver.count_occurences(solver.landscape)
                cnt = 0  # Counter to keep track of how many target tiles match the expected value

                # Check if the count of each target tile (1 to 4) matches the expected number
                for i in range(1, 5):
                    if digits.get(i) == solver.targets.get(i):  # Compare the count of the target tile with the expected value
                        cnt += 1  # Increment the counter if the target tile count matches

                # Assert that exactly 4 of the target tiles match
                self.assertEqual(
                    cnt,  # The actual count of matching target tiles
                    4,  # The expected count of matching target tiles
                    f"Test failed for {filepath}: expected 4 of target to be equal but got {cnt} equal !"  # Failure message if the test fails
                )
            
            # Log that the current file has passed the unit test
            print(f'Completed {filepath}. It passed unit test !')
        
        # Log that all test cases passed successfully
        print('Test cases has passed unit test !')

# This block runs the unit test when the script is executed directly
if __name__ == '__main__':
    unittest.main()  # Run the unit tests defined in the TileReplacementUnitTest class
