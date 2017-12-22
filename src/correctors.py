

class Corrector:

    def __init__(self, json_words):
        self.words = [w[1] for w in json_words]
        self.something_happened = False

    def correct(self, 

class Replacer(Corrector):
   
    def is_year(number):
        """ 
        A simple function to test if the input (string or number) is a year (between 1750 and 2100). 
        """
        try:
            number = int(number)
            return number > 1750 and number < 2100
        except (ValueError, TypeError):
            return False; 

    def number_to_text(number):
        """ 
        No longer necessary for the shared task; this function converts an integer
        to its lexical string representation if this is according to the rules of OnzeTaal
        (https://onzetaal.nl/taaladvies/getallen-in-letters-of-cijfers/). 
        """
        try:
            if number >=0 and number <= 20:
                return ["nul", "een", "twee", "drie", "vier", "vijf", "zes", "zeven",
                        "acht", "negen", "tien", "elf", "twaalf", "dertien", "veertien",
                        "vijftien", "zestien", "zeventien", "achttien", "negentien", "twintig"][number]
            elif not number%10 and number <= 100:
                return ["dertig", "veertig", "vijftig", "zestig",
                        "zeventig", "tachtig", "negentig", "honderd"][int(number/10)-3]
            elif not number%100 and number <= 1000:
                return ["tweehonderd", "driehonderd", "vierhonderd", "vijfhonderd", "zeshonderd",
                        "zevenhonderd", "achthonderd", "negenhonderd", "duizend"][int(number/100)-2]
            elif not number%1000 and number <= 12000:
                return ["tweeduizend", "drieduizend", "vierduizend", "vijfduizend", "zesduizend", "zevenduizend",
                        "achtduizend", "negenduizend", "tienduizend", "elfduizend", "twaalfduizend"][int(number/1000)-2]
            else:
                return str(number)
        except TypeError:
            return number;


class Splitter(Corrector):

class Inserter(Corrector):

class Attacher(Corrector):


class Correctors:
    self.replacer = Replacer()
    self.splitter = Splitter()
    self.inserter = Inserter()
    self.attacher = Attacher()

    



    def replaceables_window(ws):
        """
        This function tries to find a replaceable in the window 'a b c d e' for word 'c'.
        It creates a correction with the superclass 'replace', and more specific classes
        such as 'capitalizationerror', 'redundantpunctuation', 'nonworderror' and the wildcard
        'replace'. It implicitely also finds archaic and confuseables, but there are shared
        under the class 'replace'.
        
        It follows a backoff strategy, where it starts with window size 5, 2 on the left, 2 on 
        the right. If there is not a word 'c'' with a higher frequency, then it backs off to 
        a 3 word window. Analoguously it finally also tries if a word without context might be
        a better fit if the word 'c' seems to be out-of-vocabulary.
        
        Returns a triple (r1, r2, r3) where
            r1 = a correction has been found,
            r2 = the 'new' window, with word 'c' being replaced,
            r3 = the correction.
            
        >>> wss = create_internal_sentence(create_sentence("Speer bij de processen van Neurenberg".split(), 'page1.text.div.5.p.2.s.1'))
        >>> for w in window(wss, 5):
                print(replaceables_window(w))
        (False, 'Speer bij de processen van', {'superclass': 'replace', 'class': 'capitalizationerror', 'span': ['page1.text.div.5.p.2.s.1.w.3'], 'text': 'de'})
        (True, 'bij de Processen van Neurenberg', {'superclass': 'replace', 'class': 'capitalizationerror', 'span': ['page1.text.div.5.p.2.s.1.w.4'], 'text': 'Processen'})
        """
        words = [w[1] for w in ws]

        something_happened = False

        c = ws[2][1]

        best_s = bp(" ".join(words))
        best_f = fr(best_s)
        best_w = c

        # Do not convert 2,5 into 25
        if is_year(c) or c.translate(punct_translator).isdigit() or c in string.punctuation:
            return (False, best_s, {})

        local_threshold = replace_threshold

        # 2-2 word context
        for word in all_words:
            if not word.unknown() and Levenshtein.distance(ts(word), c) < 2:
                a_b_X_d_e = " ".join(words[0:2] + [ts(word)] + words[3:5])
                p_a_b_X_d_e, f_a_b_X_d_e = pf_from_cache(a_b_X_d_e)

                if f_a_b_X_d_e*local_threshold > best_f:
                    something_happened = True
                    best_f = f_a_b_X_d_e
                    best_s = a_b_X_d_e
                    best_w = ts(word)
                    print("nee")

        

        # 1-1 word context
        if not something_happened:
            best_f = fr(" ".join(words[1:4]))
            print(str(best_f) + "\t" + " ".join(words[1:4]))
            for word in all_words:
                if not word.unknown() and Levenshtein.distance(ts(word), c) < 2:
                    a_b_X_d_e = " ".join(words[1:2] + [ts(word)] + words[3:4])               
                    p_a_b_X_d_e, f_a_b_X_d_e = pf_from_cache(a_b_X_d_e)
                                   
                    if f_a_b_X_d_e/local_threshold > best_f and fr(" ".join(words[1:2] + [ts(word)] + words[3:5])) >= fr(" ".join(words[1:5])):
                        something_happened = True
                        best_f = f_a_b_X_d_e
                        best_s = a_b_X_d_e
                        best_w = ts(word)
            if something_happened:
                best_s = ws[0][1] + " " + best_s + " " + ws[4][1]

        # no context
        if not something_happened and not model.occurrencecount(ws[2][2]):
            for word in all_words:
                if not word.unknown() and Levenshtein.distance(ts(word), c) < 2:
                    f = fr(word);
                    if f > best_f:
                        something_happened = True
                        best_f = f
                        best_w = ts(word)
            if something_happened:
                best_s = ws[0][1] + " " + ws[1][1] + " " + best_w + " " + ws[3][1] + " " + ws[4][1]
        


        correction = {}
        correction['superclass'] = "replace"
        if c.lower() == best_w.lower():
            correction['class'] = "capitalizationerror"
        elif c.translate(punct_translator) == best_w.translate(punct_translator) or unidecode.unidecode(c) == unidecode.unidecode(best_w):
            correction['class'] = "redundantpunctuation"
        elif not model.occurrencecount(ws[2][2]):
            correction['class'] = "nonworderror"
        else:
            correction['class'] = "replace"
        correction['span'] = [ws[2][0]]
        correction['text'] = best_w
        return (something_happened and best_s != " ".join(words), best_s, correction)

    def pf_from_cache(candidate):
        """
        If candidate is already in the pattern-frequency cache, then retrieve its
        colibricore.Pattern representation and its frequency. Otherwise compute the
        values and put it in the cache first.
        
        >>> pf_from_cache("patroon")
        (<colibricore.Pattern at 0x7f253d1c68d0>, 1.4490891920364536e-05)
        """
        if False and candidate in p_cache:
            (p_candidate, f_candidate) = p_cache[candidate]
        else:
            p_candidate = classencoder.buildpattern(candidate)
            f_candidate = fr(p_candidate)
            #p_cache[candidate] = (p_candidate, f_candidate)
        return (p_candidate, f_candidate)

    def runon_errors_window(ws):
        """
        This function tries to find runon errors in the window 'a b c d e' for the words
        'c' and 'd'. If the frequency of 'cd' is higher than 'c d' (notice the the order
        of the window is now different), it replaces 'c d' with 'cd'.
        
        Returns a triple (r1, r2, r3) where
            r1 = a correction has been found,
            r2 = the 'new' window, with word 'c d' being replaced for 'cd',
            r3 = the correction.
        
        >>> wss = create_internal_sentence(create_sentence("in de wapenindustrie tewerk waren gesteld".split(), 'page1.text.div.5.p.2.s.1'))
        >>> for w in window(wss, 5):
                print(runon_errors_window(w))
        (False, <colibricore.Pattern object at 0x7f253d1c6790>, {'class': 'runonerror', 'span': ['page1.text.div.5.p.2.s.1.w.3'], 'text': 'wapenindustrie'})
        (True, 'de wapenindustrie te werk waren gesteld', {'class': 'runonerror', 'span': ['page1.text.div.5.p.2.s.1.w.4'], 'text': 'te werk'})
        """
        words = [w[1] for w in ws]

        something_happened = False

        middle = words[2]#"".join(words[2:4])

        best_s = classencoder.buildpattern(" ".join(words))
        best_candidate = middle
        best_f = fr(ws[2][2])

        for x in range(len(middle)+1):
            candidate = copy.copy(middle)
            candidate = '{0} {1}'.format(candidate[:x], candidate[x:])

            p_candidate, f_candidate = pf_from_cache(candidate)
            
            if f_candidate > best_f  and not bp(candidate[:x]).unknown() and not bp(candidate[x:]).unknown():# and s_candidate.strip().split(" "):
                something_happened = True
                best_f = f_candidate
                best_s = " ".join(ws[0][1] + ws[1][1] + candidate + ws[3][1] + ws[4][1])
                best_candidate = candidate

        correction = {'class': "runonerror", 'span': [ws[2][0]], 'text': best_candidate}
        return (something_happened, best_s, correction)

    def split_errors_window(ws):
        """
        This function tries to find split errors in the window 'a b cd e' for the words
        'c' and 'd'. If the frequency of 'c d' is higher than 'cd' (notice the the order
        of the window is now different), it replaces 'c d' with 'cd'. The space is
        inserted on all possible places, and the best match is choosen to be candidate
        for the correction
        
        Returns a triple (r1, r2, r3) where
            r1 = a correction has been found,
            r2 = the 'new' window, with word 'cd' being replaced for 'c d',
            r3 = the correction.
            
        >>> wss = create_internal_sentence(create_sentence("tot 10 jaar gevangenisstraf , voornamelijk".split(), 'page1.text.div.5.p.2.s.1'))
        >>> for w in window(wss, 5):
                print(split_errors_window(w))
        (False, <colibricore.Pattern object at 0x7f253d1c6e30>, {'class': 'spliterror', 'span': '', 'text': 'jaar gevangenisstraf'})
        (True, '10 jaar gevangenisstraf, voornamelijk', {'class': 'spliterror', 'span': ['page1.text.div.5.p.2.s.1.w.4', 'page1.text.div.5.p.2.s.1.w.5'], 'text': 'gevangenisstraf,'})

        """
        words = [w[1] for w in ws]

        something_happened = False

        best_s = bp(" ".join(words))
        best_candidate = ws[2][1] + " " + ws[3][1] + " " + ws[4][1]
        best_f = fr(best_candidate)
        best_span = ""

        a_b_cd_e = ws[2][1]+ws[3][1] + " " + ws[4][1]
       
        p_a_b_cd_e, f_a_b_cd_e = pf_from_cache(a_b_cd_e)

        if not p_a_b_cd_e.unknown() and f_a_b_cd_e > best_f:# and not oc(classencoder.buildpattern(ws[1][1]+" "+ws[2][1])):
            something_happened = True
            best_f = f_a_b_cd_e
            best_s = ws[0][1] + " " + ws[1][1] + " " + ws[2][1]+ws[3][1] + " " + ws[4][1]
            best_candidate = ws[2][1] + ws[3][1]
            best_span = [ws[2][0],ws[3][0]]

        correction = {'class': "spliterror", 'span': best_span, 'text': best_candidate}
        return (something_happened, best_s, correction)


    p_cache = {}


    def missing_words_window(ws):
        """
        This function tries to find a missing word in the window 'a b c d e' after the
        word 'c'. If the frequency of 'c f d' is higher than 'c d' (notice that the order
        of the window is now different), it inserts 'f' after 'c'.
        
        Returns a triple (r1, r2, r3) where
            r1 = a correction has been found,
            r2 = the 'new' window, with word 'f' being inserted after 'c',
            r3 = the correction.
        """
        words = [w[1] for w in ws]

        # at most 1 insertion
        if ws[3][0].endswith("M") or ws[2][0].endswith("M"):
            return (False, "", {})

        something_happened = False
        #
        joinwords = " ".join(words)
        best_s = bp(joinwords)
        best_f = fr(" ".join(words[0:3] + words[3:4]))#fr(best_s)
        best_w = ""

        #
        for word in all_words:
            if not word.unknown():
                tsword = ts(word)
                a_b_c_X_d_e = " ".join(words[0:3] +[tsword] + words[3:4])
                p_a_b_c_X_d_e, f_a_b_c_X_d_e = pf_from_cache(a_b_c_X_d_e)
                    
                if f_a_b_c_X_d_e > best_f:
                    something_happened = True
                    best_f = f_a_b_c_X_d_e
                    best_s = a_b_c_X_d_e
                    best_w = tsword
            # backoff option?
        correction = {'class': "missingword", 'after': ws[2][0], 'text': best_w}
        return (something_happened and best_s != joinwords, best_s, correction)