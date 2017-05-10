import cssutils

def getStyleRules(rules):
    result = []
    for rule in rules:
        if isinstance(rule, cssutils.css.CSSMediaRule):
            result = result + getStyleRules(rule.cssRules)
        elif isinstance(rule, cssutils.css.CSSComment):
            continue
        elif isinstance(rule, cssutils.css.CSSUnknownRule):
            continue
        else:
            result.append(rule)
    return result

def getMediaText(rule):
    if rule.parentRule is None:
        return ""
    
    return rule.parentRule.media.mediaText

def isDuplicate(rule1, rule2):
    if rule1.selectorText != rule2.selectorText:
        return False
    if rule1.cssText != rule2.cssText:
        return False
    if getMediaText(rule1) != getMediaText(rule2):
        return False
    return True

def printDuplicates (rules):
    index = 0
    for rule1 in rules:
        index = index + 1
        for rule2 in rules[index:]:
            if rule1 != rule2 and isDuplicate(rule1, rule2):
                if rule1.parentRule is not None and rule2.parentRule is not None:
                    print rule1.parentRule.media.mediaText
                    print rule2.parentRule.media.mediaText
                    print rule1.parentRule.media.mediaText == rule2.parentRule.media.mediaText
                print rule1.selectorText
                print rule2.selectorText
                print "\n"

def cleanmediarule(mediarule):
    ''' Remove any duplicate styles from this media query '''
    rules = []
    for index, rule in enumerate(mediarule.cssRules):
        if not isinstance(rule, cssutils.css.CSSStyleRule):
            continue
        dupadded = False
        for addedrule in rules:
            # If this selector is already in the list, it's a dup
            if addedrule.selectorText == rule.selectorText and addedrule.cssText == rule.cssText:
                mediarule.deleteRule(index)
                dupadded = True
                break
        if not dupadded:
            rules.append(rule)

def combinemediarules(sheet):
    ''' Combine all classes from identical media rules into the same rule '''
    rules = []
    index = 0
    cssRulesCopy = sheet.cssRules[:]
    for rule in cssRulesCopy:
        if not isinstance(rule, cssutils.css.CSSMediaRule):
            index = index + 1
            continue
        dupadded = False
        for addedrule in rules:
            # If this selector is already in the list, it's a dup
            if addedrule.media.mediaText == rule.media.mediaText:
                for rule_to_move in rule.cssRules:
                    addedrule.add(rule_to_move)
                sheet.deleteRule(index)
                dupadded = True
                break
        if not dupadded:
            rules.append(rule)
            index = index + 1

def cmp_rules(x, y):
    if isinstance(x, cssutils.css.CSSMediaRule) and isinstance(y, cssutils.css.CSSMediaRule):
        return cmp(x.media.mediaText, y.media.mediaText)
    if isinstance(x, cssutils.css.CSSComment) or isinstance(y, cssutils.css.CSSComment):
        return 0
    else:
        return 0 #cmp(x, y)

def main():
    ''' Main process '''
    parser = cssutils.CSSParser(validate=False)

    print "[PARSING FILE]"
    css = open("responsive_ceu.css")
    stylesheet = parser.parseString(css.read())
    css.close()

    print "[FINISHED PARSING FILE]"
    print "[COMBINING MEDIA RULES]"

    combinemediarules(stylesheet)

    print "[CLEANING MEDIA RULES]"
    for rule in stylesheet.cssRules:
        if isinstance(rule, cssutils.css.CSSMediaRule):
            cleanmediarule(rule)

    # rules = getStyleRules(stylesheet.cssRules)
    # printDuplicates(rules)

    # stylesheet.cssRules.sort(cmp=cmp_rules, reverse=True)


    # Print the stylesheet to a new file
    cssutils.ser.prefs.indentClosingBrace = False
    cssutils.ser.prefs.omitLastSemicolon = False
    cssutils.ser.prefs.listItemSpacer = "\n"

    outputfile = open('responsive_ceu_CLEAN.css', 'w')
    outputfile.write(stylesheet.cssText)
    outputfile.close()

    print "[FINISHED]"


if __name__ == '__main__':
    main()

