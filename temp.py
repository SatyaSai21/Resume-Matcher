
import sys
print(sys.path)
print("\n")
import setuptools
print(setuptools.find_packages())

from resume.resume_matcher.scripts.get_score import custom_test
print("\n")
print(f"================{custom_test()}================")
print("\n")
# from resume.resume_matcher.run_first import run_first
# print("\n")
# print(f"================{run_first()}================")
# print("\n")