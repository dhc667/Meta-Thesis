def fix_text(s: str) -> str:
  tilde = {'a': 'á', 'e': 'é', 'i': 'í', 'o': 'ó', 'u': 'ú', 'n': 'ñ'}

  result = ''; i = 0
  while i < len(s):
    if i + 1 < len(s):
      if s[i] == '´' or s[i] == '˜':
        i += 1
        while s[i] == ' ': i += 1
        result += tilde[s[i]]
      else:
        result += s[i]
    else:
      result += s[i]
    i += 1

  return result