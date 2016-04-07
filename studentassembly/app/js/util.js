export const capitalizeFirstLetter = (string) => {
  let smallWords = /^(a|an|and|as|at|but|by|en|for|if|in|nor|of|on|or|per|the|to|vs?\.?|via)$/

  if (!smallWords.test(string))
    return string.charAt(0).toUpperCase() + string.slice(1)
  else
    return string
}

export const toTitleCase = (string, separator = '-') => {
  return string.split(separator).map((text) => { return capitalizeFirstLetter(text) }).join(' ')
}
