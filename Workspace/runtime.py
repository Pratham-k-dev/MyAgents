import sys
sys.path.insert(0, r"C:\web dev\AI\Agents-Framework")
sys.path.insert(0, r"C:\web dev\AI")

from mytools import *
from myagents.tools import *

results = duckduckgo_search.execute(query="current monsoon news Pune 2024")
print(results.output)