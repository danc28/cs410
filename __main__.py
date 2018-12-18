from songs import users_top_tracks
from songs import playlist_tracks
from lyric import lyrics_from_genius
import nltk
nltk.download('punkt')
nltk.download('stopwords')
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
import gensim
from gensim import corpora, models
import pickle
import pyLDAvis

def tokenize_lyrics(text):
    tokenizer = RegexpTokenizer(r'\w+')
    text = text.lower()
    words = tokenizer.tokenize(text)

    tokens = []
    stop_words = stopwords.words('english')
    additional_stopwords = "a able about above abst accordance according accordingly across act actually added adj affected affecting affects after afterwards again against ah all almost alone along already also although always am among amongst an and announce another any anybody anyhow anymore anyone anything anyway anyways anywhere apparently approximately are aren arent arise around as aside ask asking at auth available away awfully b back be became because become becomes becoming been before beforehand begin beginning beginnings begins behind being believe below beside besides between beyond biol both brief briefly but by c ca came can cannot can't cause causes certain certainly co com come comes contain containing contains could couldnt d date did didn't different do does doesn't doing done don't down downwards due during e each ed edu effect eg eight eighty either else elsewhere end ending enough especially et et-al etc even ever every everybody everyone everything everywhere ex except f far few ff fifth first five fix followed following follows for former formerly forth found four from further furthermore g gave get gets getting give given gives giving go goes gone got gotten h had happens hardly has hasn't have haven't having he hed hence her here hereafter hereby herein heres hereupon hers herself hes hi hid him himself his hither home how howbeit however hundred i id ie if i'll im immediate immediately importance important in inc indeed index information instead into invention inward is isn't it itd it'll its itself i've j just k keep keeps kept kg km know known knows l largely last lately later latter latterly least less lest let lets like liked likely line little 'll look looking looks ltd m made mainly make makes many may maybe me mean means meantime meanwhile merely mg might million miss ml more moreover most mostly mr mrs much mug must my myself n na name namely nay nd near nearly necessarily necessary need needs neither never nevertheless new next nine ninety no nobody non none nonetheless noone nor normally nos not noted nothing now nowhere o obtain obtained obviously of off often oh ok okay old omitted on once one ones only onto or ord other others otherwise ought our ours ourselves out outside over overall owing own p page pages part particular particularly past per perhaps placed please plus poorly possible possibly potentially pp predominantly present previously primarily probably promptly proud provides put q que quickly quite qv r ran rather rd re readily really recent recently ref refs regarding regardless regards related relatively research respectively resulted resulting results right run s said same saw say saying says sec section see seeing seem seemed seeming seems seen self selves sent seven several shall she shed she'll shes should shouldn't show showed shown showns shows significant significantly similar similarly since six slightly so some somebody somehow someone somethan something sometime sometimes somewhat somewhere soon sorry specifically specified specify specifying still stop strongly sub substantially successfully such sufficiently suggest sup sure	t take taken taking tell tends th than thank thanks thanx that that'll thats that've the their theirs them themselves then thence there thereafter thereby thered therefore therein there'll thereof therere theres thereto thereupon there've these they theyd they'll theyre they've think this those thou though thoughh thousand throug through throughout thru thus til tip to together too took toward towards tried tries truly try trying ts twice two u un under unfortunately unless unlike unlikely until unto up upon ups us use used useful usefully usefulness uses using usually v value various 've very via viz vol vols vs w want wants was wasnt way we wed welcome we'll went were werent we've what whatever what'll whats when whence whenever where whereafter whereas whereby wherein wheres whereupon wherever whether which while whim whither who whod whoever whole who'll whom whomever whos whose why widely willing wish with within without wont words world would wouldnt www x y yes yet you youd you'll your youre yours yourself yourselves you've z zero 1 2 3 4 5 6 7 8 9 0"
    stop_words.append('chorus')
    stop_words.append('verse')
    stop_words.append('bridge')
    stop_words.append('introduction')
    stop_words.append('intro')
    stop_words.append('interlude')
    stop_words.append('hook')
    stop_words.append('instrument')

    stop_words.append('la')
    stop_words.append('bah')
    stop_words.append('uh')
    stop_words.append('unh')
    stop_words.append('yeah')
    stop_words.append('ya')
    stop_words.append('hey')
    stop_words.append('nae')
    stop_words += additional_stopwords.split()
    for w in words:
        if w not in stop_words:
            tokens.append(w)

    stems = []
    stemmer = SnowballStemmer("english")
    for token in tokens:
        token = stemmer.stem(token)
        if token != "":
            stems.append(token)
    return stems

def topic_modelling(docs):
    dictionary = corpora.Dictionary(lyric_collection)
    corpus = [dictionary.doc2bow(text) for text in lyric_collection]

    pickle.dump(corpus, open('corpus.pkl', 'wb'))
    dictionary.save('dictionary.gensim')

    NUM_TOPICS = 4
    ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics = NUM_TOPICS, id2word=dictionary, passes=20)
    ldamodel.save('model5.gensim')
    topics = ldamodel.print_topics(num_words=4)

    return topics

if __name__ == '__main__':
    track_docs = []
    username = "22gkfie5pgkyn5ect6h3nixji" #my user id from Spotify 22gkfie5pgkyn5ect6h3nixji
    track_info = users_top_tracks(username)
    print("Number of tracks grabbed is " + str(len(track_info)))
    for i in track_info:
        track_lyrics = lyrics_from_genius(i[0], i[1])
        if(track_lyrics):
            track_docs.append(track_lyrics)
    print("Number of track lyrics found is " + str(len(track_docs)))
    lyric_collection = []
    for j in track_docs:
        lyric_collection.append(tokenize_lyrics(j))
    topics = topic_modelling(lyric_collection)
    for topic in topics:
        print(topic)

    # dictionary_vis = gensim.corpora.Dictionary.load('dictionary.gensim')
    # corpus_vis = pickle.load(open('corpus.pkl', 'rb'))
    # lda = gensim.models.ldamodel.LdaModel.load('model5.gensim')
    # import pyLDAvis.gensim
    # lda_display = pyLDAvis.gensim.prepare(lda, corpus_vis, dictionary_vis, sort_topics=False)
    # pyLDAvis.enable_notebook()
    # pyLDAvis.display(lda_display)
