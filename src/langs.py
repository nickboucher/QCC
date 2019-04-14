qasm_lang = "qasm"
quil_lang = "quil"
ibm01_lang = "ibm01"

asm_langs = [qasm_lang, quil_lang]
hw_langs = [ibm01_lang]

direct_compile_from = {
    ibm01_lang: qasm_lang
}
