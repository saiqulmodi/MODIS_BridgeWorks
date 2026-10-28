const I18N = {
    current: localStorage.getItem("bridgeworks_lang") || "en",
    locales: { en: lang_en, hi: lang_hi, bn: lang_bn },
    t(key) {
        return (this.locales[this.current] && this.locales[this.current][key]) || this.locales.en[key] || key;
    },
    setLang(code) {
        if (this.locales[code]) {
            this.current = code;
            localStorage.setItem("bridgeworks_lang", code);
            location.reload();
        }
    }
};
