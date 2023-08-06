import pylabeador
import re
import stanza
import silabeador
processor_dict = {
    'tokenize': 'ancora',
    'mwt': 'ancora',
    'pos': 'ancora'
    # 'alt': 'gsd',
}

config = {
    'lang':  'es',
    'processors': processor_dict,
    'package': 'None'
}

nlp = stanza.Pipeline(**config)


class lineatexto:
    tonicos = ['yo', 'vos', 'es', 'soy', 'voy', 'sois', 'vais', 'ti']
    postonicos = ['VERB', 'ADV', 'NOUN', 'PROPN', 'ADJ', 'AUX', 'INTJ', 'NUM',
                  'DET.Dem', 'DET.Int', 'DET.Ind', 'PRON.Com', 'PRON.Nom']
    detat = ['el', 'la', 'los', 'las', 'mi', 'tu', 'su', 'nuestro', 'vuestro',
             'me', 'te', 'le', 'nos', 'os', 'les', 'lo', 'se', 'mis', 'tus',
             'sus', 'nuestros', 'vuestros']
    conjat = ['y', 'e', 'ni', 'o', 'u', 'que', 'pero', 'sino', 'mas', 'aunque',
              'pues', 'porque', 'como', 'pues', 'luego', 'conque', 'si',
              'cuando', 'aunque', 'aun cuando',
              'que', 'cual', 'quien', 'donde', 'cuando', 'cuanto', 'como']
    posat = ['ADP', 'DET.Def', 'DET.Poss']
    demostrativos = ['aqueste', 'aquesta', 'aquestos', 'aquestas', 'aquese',
                     'aquesa', 'aquesas', 'aquesos', 'este', 'esta', 'esto',
                     'estos', 'estas', 'ese', 'esos', 'esa', 'esas', 'eso',
                     'aquel', 'aquella', 'aquellos', 'aquellas']
    numeros = ['uno', 'una', 'dos', 'tres', 'cuatro', 'cinco', 'seis', 'siete',
               'ocho', 'nueve']
    cortesia = ['don', 'doña', 'sor', 'fray', 'santo']

    def __init__(self, linea):
        self.linea = linea
        self.__nlplinea = self.__postag()
        self.__p = self.__pos()
        self.n = self.__p[0]
        self.palabras = self.__p[1]
        self.silabas = self.__p[2]
        self.palasil = self.__p[3]

    def __postag(self):
        simbolos = {'(': '.', ')': '.', '—': '. ', '…': '.', ',': '. ',
                    ';': '.', ':': '.', '?': '.', '!': '.',
                    'õ': 'o', 'æ': 'ae',
                    'à': 'a', 'è': 'e', 'ì': 'i', 'ò': 'o', 'ù': 'u'}
        plinea = self.linea
        if self.linea != self.linea:
            plinea = 'aeioiu'
        else:
            for i in simbolos:
                plinea = plinea.replace(i, simbolos[i])
            plinea = re.sub(r'\.+(\w)', r'\1', plinea)
            plinea = re.sub(r'\[|\]|¿|¡|^\s*\.+|»|«|“|”|‘|’|"|-|–', '',
                            plinea)
            plinea = re.sub(r'\s*\.[\.\s]+', '. ', plinea)
            plinea = plinea.strip()
            plinea = plinea[0].upper()+plinea[1:]
        return nlp(plinea)

    @staticmethod
    def __parse_feats(feats):
        dd = {}
        if feats:
            cosas = feats.split("|")
            for i in cosas:
                feature = i.split("=")
                dd[f'{feature[0]}'] = feature[1]
        else:
            dd['None'] = 'None'
        return dd

    @staticmethod
    def acento_pros(palabra):
        if len(palabra) == 1:
            tonica = -1
        elif len(palabra) > 2 and any(k in 'áéíóúÁÉÍÓÚ' for k in palabra[-3]):
            tonica = -3
        else:
            if any(k in 'áéíóúÁÉÍÓÚ' for k in palabra[-2]):
                tonica = -2
            elif any(k in 'áéíóúÁÉÍÓÚ' for k in palabra[-1]):
                tonica = -1
            else:
                if (palabra[-1][-1] in 'nsNS' or
                        palabra[-1][-1] in 'aeiouAEIOU'):
                    tonica = -2
                else:
                    tonica = -1
        return tonica

    def silabea(self, palpos):
        dieresis = {'ä': 'a', 'ë': 'e', 'ï': 'i', 'ö': 'o', 'ü': 'u'}
        import string
        pos = palpos[1]
        palabra = palpos[0].translate(str.maketrans('', '',
                                                    string.punctuation))
        palabra = ''.join([j.lower() for j in palabra if j.isalpha()])
        x = ''.join([value for value in palabra if value in dieresis])
        if x and ('güe' not in palabra and 'güi' not in palabra):
            palabras = re.sub(x, f'{dieresis[x]} ', palabra).split()
            #silabas = [pylabeador.syllabify(y) for y in palabras]
            silabas = [silabeador.silabea(y) for y in palabras]
            silabas = [inner for outer in silabas for inner in outer]
        else:
            try:
                silabas = [item for item in pylabeador.syllabify(palabra)]
            except Exception:
                palabra = palabra.replace('y', 'i')
                silabas = [item for item in pylabeador.syllabify(palabra)]
        #tonica = self.acento_pros(silabas)
        tonica = silabeador.tonica_s(silabas)
        if (pos in self.posat or palabra in self.detat) or (
                (pos == 'CCONJ' or pos == 'SCONJ') and palabra in self.conjat):
            tonica = 0
        if tonica < 0:
            silabas[tonica] = silabas[tonica].upper()
        else:
            silabas[-1] = silabas[-1].lower()
        return(silabas)

    def __pos(self):
        listsil = []
        listpal = []
        listpalasil = []
        features = {}
        count = 0
        numflag = 0
        propnflag = 0
        nounflag = 0
        abece = {'B': 'Be', 'C': 'Ce', 'D': 'De', 'F': 'Efe', 'G': 'Ge',
                 'H': 'Hache', 'J': 'Jota', 'K': 'Ka', 'L': 'Ele', 'M': 'Eme',
                 'N': 'Ene', 'P': 'Pe', 'Q': 'Ku', 'R': 'Erre', 'S': 'Ese',
                 'T': 'Te', 'V': 'Uve', 'X': 'Equis', 'Z': 'Zeta'}
        for sentence in self.__nlplinea.sentences:
            listpala = []
            listpalsila = []
            listsila = []
            en_mente = []
            palabras = [x for x in sentence.words
                        if not (x.pos == 'PUNCT' and
                                not re.match('\w', x.text))
                        and x.pos != 'X']
            if len(palabras) > 1:
                if (palabras[-1].parent.text == palabras[-2].parent.text and
                        palabras[-1].text != palabras[-2].text):
                    palabras[-2].text = palabras[-2].parent.text
                    palabras.pop()
            for palabra in palabras:
                if len(palabra.text) > 5 and palabra.text.endswith('mente'):
                    pal1 = pal2 = palabra
                    pal1.text = palabra.text.rstrip('mente')
                    palabra.text = 'mente'
                    en_mente = en_mente + [pal1, palabra]
                else:
                    en_mente = en_mente + [palabra]
            palabras = en_mente
            for idx, word in enumerate(palabras[::-1]):
                if len(word.text) > 1:
                    word.text = word.text.strip('.')
                if idx == 0:
                    word.pos = 'NOUN'
                    features = "{'Gender': 'Masc', 'Number': 'Sing'}"
                elif not word.feats:
                    word.feats = 'PronType=None'
                elif word.text in abece:
                    word.text = abece[word.text]
                    word.pos = 'NOUN'
                elif word.pos == 'PUNCT':
                    word.pos = 'VERB'
                elif 1 < 0:
                    word.pos = 'NOUN'
                else:
                    if not word.pos:
                        continue
                    if word.text in lineatexto.conjat:
                        word.pos = 'CCONJ'
                        if word.text.lower() != 'y':
                            numflag = 0
                        features = self.__parse_feats(word.feats)
                    if word.pos == ('NUM' and word.text not in self.numeros
                                    and numflag == 1):
                        word.pos = 'DET'
                        word.feats = (word.feats+'|Definite=Def|PronType=Art')
                        features = self.__parse_feats(word.feats)
                    else:
                        numflag = 1
                    if word.pos == 'PROPN' or word.text in [x.lower()
                                                            for x in
                                                            self.cortesia]:
                        if propnflag == 1:
                            if word.text.lower() in self.demostrativos:
                                word.pos = 'DET'
                                if word.feats:
                                    word.feats = word.feats+'|PronType=Dem'
                            else:
                                word.pos = 'DET'
                                word.feats += '|Definite=Def|PronType=Art'
                        else:
                            propnflag = 1
                    else:
                        propnflag = 0
                    features = self.__parse_feats(word.feats)

                    if word.pos == 'DET':
                        if features['PronType'] == 'Dem':
                            word.pos = 'DET.Dem'
                        elif word.text in self.demostrativos:
                            word.pos = 'DET.Dem'
                        elif features['PronType'] == ('Prs' and
                                                      'Poss' in features):
                            if features['Poss'] == 'Yes':
                                if nounflag == 1:
                                    word.pos = 'DET.Poss'
                                else:
                                    word.pos = 'ADJ'
                            elif features['Case'] == 'Acc,Dat':
                                word.pos = 'DET.Art'
                                word.feats = (word.feats +
                                              '|Definite=Def|PronType=Art')
                                features = self.__parse_feats(word.feats)
                        elif features['PronType'] == 'Int,Rel':
                            word.pos = "DET.Int"
                        elif features['PronType'] == 'Ind':
                            word.pos = 'DET.Ind'
                        elif features['PronType'] == 'Tot':
                            word.pos = 'ADJ'
                        elif features['PronType'] == 'Neg':
                            word.pos = 'ADJ'
                        elif 'Definite' in features:
                            word.pos = f'DET.{features["Definite"]}'
                        else:
                            word.pos = 'DET.Def'
                    if word.pos == 'PROPN' or word.pos == 'NOUN':
                        nounflag = 1
                    else:
                        nounflag = 0
                    if word.pos == 'PRON':
                        if features['PronType'] == 'Prs':
                            if 'Case' not in features.keys():
                                features['Case'] = 'Com'
                                word.pos = 'PRON.Com'
                            if features['Case'] == 'Nom':
                                word.pos = 'PRON.Nom'
                if word.text.isalpha():
                    silabas = self.silabea((word.text.lower(), word.pos,
                                            features))
                    nsilabas = len(silabas)
                    if idx == 0:
                        #ac = self.acento_pros(silabas)
                        ac = silabeador.tonica_s(silabas)
                        silabas[ac] = silabas[ac].upper()
                    count = count+nsilabas
                    listpala.insert(0, word.text)
                    [listsila.insert(0, i) for i in silabas[::-1]]
                    listpalsila.insert(0, silabas)
                else:
                    pass
            listpal.insert(1, listpala)
            listsil = listsil + listsila
            listpalasil = listpalasil + listpalsila
        return (count, listpal, listsil, listpalasil)

    @staticmethod
    def pal2sil(palabras, sil):
        count = 0
        for i in len(palabras):
            for j in len(palabras[i]):
                if count < sil:
                    count += 1
                else:
                    return j


class silabas:

    def __init__(self, linea, esperadas):
        self.__linea = lineatexto(linea)
        self.__silabas = self.__corrige_vocales(self.__linea.silabas)
        self.n = len(self.__silabas)
        self.palabras = self.__linea.palabras
        self.palasil = self.__linea.palasil
        self.palasil = [self.__corrige_vocales(x) for x in self.__linea.palasil]
        self.r = self.__rima(self.palasil[-1])
        self.__longitudconrima = self.n + self.r[2]
        self.sinalefas = self.__nsinalefas(self.palasil)
        self.nucleosilabico = self.__nucleosilabico(self.__silabas)
        self.correccion = self.__corrige_metro(
            self.__silabas,
            esperadas,
            self.nucleosilabico,
            self.sinalefas,
            self.r[2])
        self.silabasmetricas = self.correccion[0]
        self.ambiguo = self.correccion[2]
        self.nucleosilabico = self.correccion[1]
        self.rima = self.r[1]
        self.ml = len(self.silabasmetricas) + self.r[2]
        self.ason = self.r[3]
        self.ritmo = self.__ritmo(self.nucleosilabico)

    @staticmethod
    def __corrige_vocales(slbs):
        a = []
        voc = {'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u', 'v': 'b',
               'qu': 'k'}
        letras = ['J', 'G', 'Z', 'K']
        for i in range(len(slbs)):
            if slbs[i][-1].lower() == 'y':
                slbs[i] = re.sub('y', 'i', slbs[i], flags=re.IGNORECASE)
            if slbs[i].isupper():
                letras = [x.upper() for x in letras]
                for key in voc.keys():
                    slbs[i] = re.sub(key, voc[key].upper(), slbs[i],
                                     flags=re.IGNORECASE)
            else:
                letras = [x.lower() for x in letras]
                for key in voc.keys():
                    slbs[i] = re.sub(key, voc[key], slbs[i],
                                     flags=re.IGNORECASE)
            slbs[i] = re.sub(r'g([ei])', rf'{letras[0]}\1', slbs[i],
                             flags=re.IGNORECASE)
            slbs[i] = re.sub(r'gu([ei])', rf'{letras[1]}\1', slbs[i],
                             flags=re.IGNORECASE)
            slbs[i] = re.sub(r'c([ei])', rf'{letras[2]}\1', slbs[i],
                             flags=re.IGNORECASE)
            slbs[i] = re.sub(r'c([aou])', rf'{letras[3]}\1', slbs[i],
                             flags=re.IGNORECASE)
            if ('h' in slbs[i].lower() and
                    'ch' not in slbs[i].lower()):
                slbs[i] = re.sub('h', '', slbs[i], flags=re.IGNORECASE)
            a.append(slbs[i])
        return a

    @staticmethod
    def __nsinalefas(palas):
        vocales = 'aeiouáéíóúAEIOUÁÉÍÓÚüÜ'
        sinalefas = []
        sineresis = []
        k = -1
        for i in range(len(palas)):
            if i > 0:
                if (palas[i][0][0] in vocales and
                        palas[i-1][-1][-1] in vocales):
                    sinalefas.append(k)
            for j in range(len(palas[i])):
                if j > 0:
                    if (
                            palas[i][j][0] in vocales and
                            palas[i][j-1][-1] in vocales):
                        if palas[i][j][0].lower() == palas[i][j-1][-1].lower():
                            sineresis.insert(0, k+j)
                        else:
                            sineresis.append(k+j)
            k += len(palas[i])
        return sinalefas + sineresis

    def __ajusta_metro(self, p, n, s):
        if len(p) < 1:
            return n
        else:
            if p[0] < len(s):
                q = []
                diptongo = s[p[0]] + s[p[0]+1]
                dmetro = n[p[0]] + n[p[0]+1]
                s[p[0]+1] = diptongo
                n[p[0]+1] = dmetro
                mayor = p[0]
                s.pop(p[0])
                n.pop(p[0])
                for x in p:
                    if x > mayor:
                        q.append(x-1)
                    else:
                        q.append(x)
                    mayor = x
                p = q
            p.pop(0)
            return(self.__ajusta_metro(p, n, s))

    @staticmethod
    def __dipt(diferencia, nucleo):
        ajuste = []
        for i in nucleo:
            if diferencia > 0 and len(i) > 1:
                ajuste += [k for k in i]
            else:
                ajuste += i
        return ajuste

    @staticmethod
    def __hiato(silabas, diferencia):
        ajuste = []
        for i in silabas:
            silaba = [i]
            if diferencia > 0:
                dip = re.search(r'(^\w*?[aeiou]{1})([aeiou]{1}.*?$)',
                                i, re.IGNORECASE)
                if dip:
                    silaba = [dip.group(1), dip.group(2)]
                    diferencia -= 1
                    if dip.group(1).isupper():
                        silaba[0] = silaba[0].lower()
                        silaba[1] = silaba[1].upper()
            ajuste = ajuste + silaba
        return ajuste

    def __corrige_metro(self, silabas, esperadas, nsilabico, sinalefas, rima):
        lon_rima = len(silabas) + rima
        offset = esperadas[0] - lon_rima
        ajustadas = silabas+[]
        sinalefasb = sinalefas+[]
        nsilabico_aj = nsilabico+[]
        ambiguo = 0
        if lon_rima == esperadas[0]:
            sinalefasb = []
        elif offset == 0:
            pass
        elif  lon_rima - len(sinalefas) == esperadas[0]:
            ajustadas = self.__ajusta_metro(sinalefasb, ajustadas,
                                            nsilabico_aj)
        else:
            ambiguo = 1
            if offset < 0:
                offset = -offset
                if len(sinalefas) >= offset:
                    ambiguo = 1
                    sinalefasb = [sinalefas[x] for x in range(offset)]
                else:
                    pass
                ajustadas = self.__ajusta_metro(sinalefasb, ajustadas,
                                                nsilabico_aj)
            else:
                ambiguo = 1
                if len(sinalefasb) >= offset:
                    sinalefasb = sinalefasb[:offset]
                    ajustadas = self.__ajusta_metro(sinalefasb, ajustadas,
                                                    nsilabico_aj)
                else:
                    ajustadas = self.__hiato(ajustadas,
                                             esperadas[0] -
                                             lon_rima - len(sinalefasb))
        nsilabico_aj = self.__nucleosilabico(ajustadas)

        if len(ajustadas) + rima != esperadas[0]:
            return self.__corrige_metro(silabas, esperadas[1:],
                                     nsilabico, sinalefas, rima)
        else:
            return (ajustadas,
                    nsilabico_aj,
                    ambiguo)

    @staticmethod
    def __nucleosilabico(slbs):
        vocalsdic = {'a': 'a', 'e': 'e', 'i': 'i', 'o': 'o', 'u': 'u',
                     'A': 'A', 'E': 'E', 'I': 'I', 'O': 'O', 'U': 'U',
                     'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U',
                     'á': 'A', 'é': 'E', 'í': 'I', 'ó': 'O', 'ú': 'U',
                     'ü': 'u', 'Ü': 'U'}
        nsbl = []
        for i in slbs:
            j = ''.join([c for c in i if c in vocalsdic])
            for k in vocalsdic:
                j = re.sub(k, vocalsdic[k], j)
            nsbl.append(j)
        return nsbl

    @staticmethod
    def __rima(palabra):
        vocales = 'aeiouáéíóúAEIOUÁÉÍÓÚüÜ'
        suma = {-1: 1, -2: 0, -3: -1}
        tonica = 0
        for idx, word in enumerate(palabra[::-1]):
            if word.isupper():
                tonica = -idx - 1
        if tonica == 0:
            #tonica = lineatexto.acento_pros(palabra)
            tonica = silabeador.tonica_s(palabra)
        ultimas = palabra[tonica:]
        ultimas[0] = re.sub(r'[IÍUÜÚ]([AEIOU])', r'\1', ultimas[0])

        r = '-'.join([c for c in ultimas])
        for j in range(len(r)):
            if r[j] not in vocales:
                pass
            else:
                t = r[j:]
                break
        ason = re.sub(r'([^AEIOUaeiou\-]+)','',t).lower()
        ason = re.sub(r'[iu]*([aeiou])[iu]*', r'\1', ason)
        ason = re.sub(r'(.\-).\-(.)',r'\1\2', ason)
        t = t.replace('-','')
        return [tonica, t, suma[tonica], ason]

    @staticmethod
    def __ritmo(nslb):
        metro = []
        for i in nslb:
            if any(x.isupper() for x in i):
                metro.append('+')
            else:
                metro.append('-')
        return ''.join(metro)
