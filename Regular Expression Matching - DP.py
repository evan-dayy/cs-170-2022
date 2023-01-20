"""
Given an input string s and a pattern p, implement regular expression matching with support for '.' and '*' where:

'.' Matches any single character.​​​​
'*' Matches zero or more of the preceding element.
The matching should cover the entire input string (not partial).
"""


class Solution(object):
    def isMatch(self, text, pattern):
        memo = {}

        def dp(i, j):
            if (i, j) in memo:
                return memo[(i, j)]
            if j == len(pattern):
                return i == len(text)
            first_match = i < len(text) and pattern[j] in {text[i], '.'}
            if j + 1 < len(pattern) and pattern[j + 1] == '*':
                memo[(i, j)] = dp(i, j + 2) or (first_match and dp(i + 1, j))
            else:
                memo[(i, j)] = first_match and dp(i + 1, j + 1)
            return memo[(i, j)]

        return dp(0, 0)


"""
Given an input string (s) and a pattern (p), implement wildcard pattern matching with support for '?' and '*' where:

'?' Matches any single character.
'*' Matches any sequence of characters (including the empty sequence).
The matching should cover the entire input string (not partial).

"""


class Solution:
    def isMatch(self, s: str, p: str) -> bool:
        n, m = len(s), len(p)

        # i is index in s, j is index in p
        @cache
        def dfs(i, j):
            if i >= n and j >= m:
                return True
            if j >= m:
                return False
            if i < n and (s[i] == p[j] or p[j] == "?"):
                return dfs(i + 1, j + 1)
            if (p[j] == "*"):
                return (i < n and dfs(i + 1, j)) or dfs(i, j + 1)
            # no wildcard and not matched (or reached end of string before reaching end of pattern)
            return False

        return dfs(0, 0)
