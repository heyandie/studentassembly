export const capitalizeFirstLetter = (str) => {
  let smallWords = /^(a|an|and|as|at|but|by|en|for|if|in|nor|of|on|or|per|the|to|vs?\.?|via)$/

  if (!smallWords.test(str))
    return str.charAt(0).toUpperCase() + str.slice(1)
  else
    return str
}

export const toTitleCase = (str, sep = '-') => {
  return str.split(sep).map((text) => { return capitalizeFirstLetter(text) }).join(' ')
}
