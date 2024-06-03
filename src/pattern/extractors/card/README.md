Data retrieved from https://docs.trellix.com/bundle/data-loss-prevention-11.10.x-classification-definitions-reference-guide/page/GUID-8A0A2E8B-D740-476E-B10C-885919573022.html, by running the following code on page

```js
function maptoregexp(elements){
    elements = Array.from(elements)
    return JSON.stringify(elements.map(el=>el.innerText), null, 2)
}
var [validator_section, positive_match_section, negative_match_section] = document.querySelectorAll("section.section")
var positive_matchers = maptoregexp(positive_match_section.querySelectorAll("code")), negative_matchers = maptoregexp(negative_match_section.querySelectorAll("code"))
var validator = validator_section.querySelector("td") && validator_section.querySelector("td").innerText, 
    description = document.querySelector(".shortdesc").innerText // Break long words at exactly 78 characters
        .replace(/([^\s]{78})/g, '$1\n\t')
        // Break long lines honoring whitespace
        .replace(/([^\n]{1,78})(\s|$)/g, '$1\n\t')
        .trim()

python_code = `
    ### The following part is automatically generated from ${location.href}
    description = """
    ${description}

    validator = ${validator}
    """
    extraction_regex_list = ${positive_matchers}
    filter_regex_list = ${negative_matchers}
    extraction_regex = "|".join(extraction_regex_list)

    #end of generated code

`

console.log(python_code)
copy(python_code)
```