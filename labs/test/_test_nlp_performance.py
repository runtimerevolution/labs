from labs.config import get_logger
from labs.nlp import NLP_Interface
from transformers import pipeline
from rouge_score import rouge_scorer
import pandas as pd

summaries = {
    "text1": {
        "original": """Albert Einstein was a theoretical physicist who developed the theory of relativity, one of the two pillars of modern physics (alongside quantum mechanics). His work is also known for its influence on the philosophy of science. He is best known to the general public for his mass–energy equivalence formula E = mc^2, which has been dubbed "the world's most famous equation". He received the 1921 Nobel Prize in Physics "for his services to theoretical physics, and especially for his discovery of the law of the photoelectric effect", a pivotal step in the development of quantum theory.

Einstein was born in the German Empire but moved to Switzerland in 1895, forsaking his German citizenship. In 1896, he enrolled in the mathematics and physics teaching diploma program at the Swiss Federal polytechnic school in Zurich, graduating in 1900. He was employed at the Swiss Patent Office in Bern while he completed his doctorate, and in 1905 he published four groundbreaking papers, which attracted the attention of the academic world. The rest of his life was spent in pursuit of various scientific and humanitarian endeavors, including efforts to combat anti-Semitism and advocate for civil rights.""",
        "50": "Einstein developed the theory of relativity.",
        "100": "Albert Einstein, creator of relativity theory, won the 1921 Nobel Prize in Physics.",
        "200": "Einstein developed relativity, known for E=mc^2. Born in Germany, he moved to Switzerland, and in 1921 won the Nobel Prize in Physics for his work on the photoelectric effect.",
        "300": "Einstein, a theoretical physicist, developed the theory of relativity and is known for E=mc^2. He won the 1921 Nobel Prize in Physics for the photoelectric effect. Born in Germany, he moved to Switzerland in 1895, studied in Zurich, and published groundbreaking papers in 1905. He also combated anti-Semitism and advocated for civil rights.",
        "500": "Albert Einstein was a theoretical physicist who developed the theory of relativity, known for E=mc^2. Born in Germany, he moved to Switzerland in 1895. He studied at the Swiss Federal Polytechnic in Zurich, graduating in 1900. While working at the Swiss Patent Office, he published groundbreaking papers in 1905. He won the 1921 Nobel Prize in Physics for his discovery of the photoelectric effect, a key quantum theory development. He also fought against anti-Semitism and advocated for civil rights.",
        "1000": "Albert Einstein, born in the German Empire, later moved to Switzerland, where he developed the theory of relativity, a pillar of modern physics alongside quantum mechanics. Best known for the mass–energy equivalence formula E=mc^2, he profoundly influenced the philosophy of science. After enrolling at the Swiss Federal Polytechnic in Zurich, he graduated in 1900 and worked at the Swiss Patent Office while completing his doctorate. His 1905 publications revolutionized physics. Awarded the 1921 Nobel Prize in Physics for the photoelectric effect discovery, he significantly contributed to quantum theory. Throughout his life, he pursued scientific and humanitarian efforts, combating anti-Semitism and advocating for civil rights."
    },
    "text2": {
        "original": """The rapid advancements in artificial intelligence (AI) and machine learning (ML) have led to significant changes in various industries, including healthcare, finance, and transportation. AI algorithms are now being used to diagnose diseases, predict stock market trends, and optimize logistics and supply chains. This technological revolution is driven by the availability of large datasets, powerful computing resources, and sophisticated algorithms.

However, the widespread adoption of AI also raises several ethical and societal concerns. Issues such as data privacy, algorithmic bias, and the potential displacement of jobs by automation are hotly debated topics. It is crucial for policymakers, technologists, and society at large to work together to ensure that the benefits of AI are realized while mitigating its risks. Future advancements in AI hold great promise but must be approached with caution and responsibility.""",
        "50": "AI transforms industries, raising ethical concerns.",
        "100": "AI and ML revolutionize industries but raise ethical and societal concerns.",
        "200": "AI and ML are transforming healthcare, finance, and transportation through algorithms that diagnose diseases, predict trends, and optimize logistics. However, ethical issues like data privacy and job displacement need addressing.",
        "300": "AI and ML are revolutionizing industries such as healthcare, finance, and transportation by diagnosing diseases, predicting market trends, and optimizing logistics. This progress is driven by large datasets and powerful computing, but raises ethical concerns like data privacy and job displacement, requiring careful oversight.",
        "500": "Rapid advancements in AI and ML are transforming industries like healthcare, finance, and transportation. AI algorithms diagnose diseases, predict stock trends, and optimize logistics. This revolution is fueled by big data, powerful computing, and advanced algorithms. However, ethical and societal concerns such as data privacy, algorithmic bias, and job displacement by automation are significant. Policymakers and technologists must collaborate to harness AI's benefits while mitigating risks, ensuring responsible and cautious advancements.",
        "1000": "Artificial intelligence (AI) and machine learning (ML) are rapidly advancing, significantly impacting various industries, including healthcare, finance, and transportation. AI algorithms are now capable of diagnosing diseases, predicting stock market trends, and optimizing logistics and supply chains, driven by the availability of large datasets, powerful computing resources, and sophisticated algorithms. However, this technological revolution brings ethical and societal concerns. Issues such as data privacy, algorithmic bias, and potential job displacement due to automation are hotly debated. Addressing these challenges requires collaboration among policymakers, technologists, and society at large to ensure the benefits of AI are realized while mitigating its risks. The future of AI holds great promise, but advancements must be approached with caution and responsibility to ensure they contribute positively to society."
    },
    "text3": {
        "original": """The Great Wall of China is a series of fortifications made of stone, brick, tamped earth, wood, and other materials, generally built along an east-to-west line across the historical northern borders of China to protect and consolidate territories of Chinese states and empires against various nomadic groups of the steppe and their polities. Several walls were built as early as the 7th century BC; these, later joined together and made bigger and stronger, are collectively referred to as the Great Wall. Especially famous is the wall built between 220–206 BC by the first Emperor of China, Qin Shi Huang. Little of that wall remains. The majority of the existing wall is from the Ming Dynasty (1368–1644).

Apart from defense, other purposes of the Great Wall have included border controls, allowing the imposition of duties on goods transported along the Silk Road, regulation or encouragement of trade, and the control of immigration and emigration. Furthermore, the defensive characteristics of the Great Wall were enhanced by the construction of watchtowers, troop barracks, garrison stations, signaling capabilities through the means of smoke or fire, and the fact that the path of the Great Wall also served as a transportation corridor.""",
        "50": "The Great Wall of China: ancient fortifications.",
        "100": "The Great Wall of China, built for defense and border control, mainly dates to the Ming Dynasty.",
        "200": "The Great Wall of China, constructed from various materials, spans across northern China. Built for defense, it also served for border control, trade regulation, and immigration control. Most of the existing wall is from the Ming Dynasty.",
        "300": "The Great Wall of China, stretching across northern China, was built from various materials for defense and border control. Begun in the 7th century BC and expanded by the Qin and Ming dynasties, it also regulated trade and immigration. Enhanced by watchtowers and signaling, it served as a transportation corridor.",
        "500": "The Great Wall of China is a series of fortifications built from stone, brick, tamped earth, wood, and other materials. It spans east to west across northern China, initially constructed to protect Chinese states and empires from nomadic groups. The earliest walls date back to the 7th century BC, with significant additions during the Qin Dynasty (220–206 BC) and the Ming Dynasty (1368–1644). Besides defense, the Wall regulated trade and controlled immigration. Enhanced by watchtowers, barracks, garrison stations, and signaling systems, it also served as a transportation corridor.",
        "1000": "The Great Wall of China, an iconic series of fortifications, was constructed using stone, brick, tamped earth, wood, and other materials, stretching along China's northern borders. Originally built to protect Chinese states and empires from nomadic invasions, the earliest sections date back to the 7th century BC. The most renowned portions were built by the first Emperor of China, Qin Shi Huang, between 220–206 BC, although little of this remains today. The majority of the existing structure was constructed during the Ming Dynasty (1368–1644). Beyond its defensive purpose, the Great Wall played crucial roles in border control, imposing duties on Silk Road trade goods, and regulating immigration and emigration. Its defensive capabilities were bolstered by watchtowers, troop barracks, garrison stations, and advanced signaling methods using smoke or fire. Additionally, the Wall's path facilitated transportation and communication across the region, making it a multifaceted historical marvel."
    },
    "text4": {
        "original": 'Add a file to print sentence "Hello World"',
        "50": 'Add a file to print sentence "Hello World"',
        "100": 'Add a file to print sentence "Hello World"',
        "200": 'Add a file to print sentence "Hello World"',
        "300": 'Add a file to print sentence "Hello World"',
        "500": 'Add a file to print sentence "Hello World"',
        "1000": 'Add a file to print sentence "Hello World"'
    },
    "text5": {
        "original": """This project consists on the development of a Rest api to manage/views: Authors, Books and Categories.

        Requirements
        
        User needs to be able to manage Authors, Books, and Categories in the app.
        Each Author can have many Books that he/her has written and each book can be included in multiple categories.
        The User should be able to view lists of Authors and Books.
        The Books should be able to be filtered by Author and by Category.
        Optional: The App should also include a page to view some basic statistics, like the number of Books per Author, or the number of Books per Category.
        Optional: To complicate the models. A book can have many instances and users can request an instance to take home with a
        requested date.
        
        Acceptance Criteria
        
        Design the model entity relation for this project:
        use Mermaid, this is supported out of the box by Github's Markdown
        Design the API endpoints, including:
        path
        request
        response
        Once the design/planning part has been taken care of and agreed upon, please create tickets/issues for each of the tasks. Having those created, their commits should respect the nomenclature used in the conventional commits:
        
        if it's a task: task/<number_of_the_ticket>/small-description;
        if it's a bug: bugfix/<number_of_the_ticket>/small-description;
        if it's a release: chore/<number_of_the_ticket>/small-description.""",
        "50": 'Develop a Rest API to manage Authors, Books...',
        "100": 'Develop a Rest API to manage Authors, Books, and Categories, with filtering and statistics...',
        "200": 'Develop a Rest API to manage Authors, Books, and Categories. Users can view lists, filter Books by Author and Category, and see statistics like the number of Books per Author or Category.',
        "300": 'Develop a Rest API to manage Authors, Books, and Categories. Users can view lists, filter Books by Author and Category, and see statistics like the number of Books per Author or Category. The app may include book instances for user requests. Design models and endpoints, create tasks/issues...',
        "500": 'Develop a Rest API to manage Authors, Books, and Categories. Users can view lists, filter Books by Author and Category, and see statistics like the number of Books per Author or Category. The app may include book instances for user requests. Design models and endpoints, create tasks/issues, and follow conventional commit nomenclature. Use Mermaid for entity relations, and plan the API paths, requests, and responses. Optional features include advanced statistics and complex book instance models...',
        "1000": 'Develop a Rest API to manage Authors, Books, and Categories. Users can view lists, filter Books by Author and Category, and see statistics like the number of Books per Author or Category. The app may include book instances for user requests. Design models and endpoints, create tasks/issues, and follow conventional commit nomenclature. Use Mermaid for entity relations, and plan the API paths, requests, and responses. Optional features include advanced statistics and complex book instance models. This project involves managing Authors, Books, and Categories in the app, where each Author can have many Books, and each book can belong to multiple categories. Users should be able to view lists of Authors and Books and filter Books by Author and Category. The app should include basic statistics and possibly a page for viewing detailed statistics, such as the number of Books per Author or Category. Additionally, the app could handle book instances, allowing users to request specific instances for a set period. The project requires careful design and planning of model entity relations using Mermaid and defining API endpoints with clear paths, requests, and responses...'
    },
    "text6": {
        "original": """The idea is to test, investigate and determine the number of minimum characters of a request string that should pass through an NLP worker in order to generate a summary text to be used in an LLM prompt.

        To do so, here are the possible tasks:
        
        Test the existing Spacy configuration with various prompts having different text lengths.
        
        Record the results
        Test the different Spacy configurations with various prompts having different text lengths.
        
        Record the results
        Investigate NLP technologies, different than Spacy.
        
        Record the results
        At the end, define the optimal, configuration for NLP:
        
        Library
        Minimum length for NLP summary""",
        "50": 'Test Spacy configs to find optimal NLP summary length...',
        "100": 'Test Spacy configurations to find the minimum request string length for optimal NLP summaries...',
        "200": 'Test Spacy configurations to find the minimum request string length for optimal NLP summaries. Record results and explore other NLP technologies for the best configuration...',
        "300": 'Test Spacy configurations to find the minimum request string length for optimal NLP summaries. Record results and explore other NLP technologies for the best configuration. Determine the optimal library and minimum length for NLP summaries to be used in LLM prompts...',
        "500": 'Test Spacy configurations to find the minimum request string length for optimal NLP summaries. Record results and explore other NLP technologies for the best configuration. Determine the optimal library and minimum length for NLP summaries to be used in LLM prompts. The project involves testing various Spacy setups with different text lengths, recording results, and comparing them with other NLP technologies. The goal is to identify the best configuration that ensures accurate and efficient summaries...',
        "1000": """The idea is to test, investigate and determine the number of minimum characters of a request string that should pass through an NLP worker in order to generate a summary text to be used in an LLM prompt.

        To do so, here are the possible tasks:
        
        Test the existing Spacy configuration with various prompts having different text lengths.
        
        Record the results
        Test the different Spacy configurations with various prompts having different text lengths.
        
        Record the results
        Investigate NLP technologies, different than Spacy.
        
        Record the results
        At the end, define the optimal, configuration for NLP:
        
        Library
        Minimum length for NLP summary"""
    },
    "text7": {
        "original": """Using postman with valid authentication tokens is possible to users to access information about who submitted each picture in the contest. This results from having all the information in one graph accessible to the frontend.""",
        "50": 'Users can access picture submission info with Postman...',
        "100": 'Users can access picture submission info with Postman using valid authentication tokens. This enables...',
        "200": 'Users can access picture submission info with Postman using valid authentication tokens. This enables viewing who submitted each picture in the contest via the frontend...',
        "300": 'Using postman with valid authentication tokens is possible to users to access information about who submitted each picture in the contest. This results from having all the information in one graph accessible to the frontend.',
        "500": 'Using postman with valid authentication tokens is possible to users to access information about who submitted each picture in the contest. This results from having all the information in one graph accessible to the frontend.',
        "1000": 'Using postman with valid authentication tokens is possible to users to access information about who submitted each picture in the contest. This results from having all the information in one graph accessible to the frontend.'
    }
}

# Function to test different text lengths
def test_spacy_summarization(text, nlp_instance, lengths):
    results = []
    for length in lengths:
        shortened_text = text[length]
        len_original = len(text['original'])
        len_shortened = len(text[length])
        percentage = min(len_shortened/len_original,1)
        summary = nlp_instance.spacy_summarization(percentage)
        results.append({
            'ref_length': int(length),
            'text_length': len_original,
            'reference_length': len_shortened,
            'summary_length': len(summary),
            'percentage': percentage,
            'summary': summary,
            'reference': shortened_text
        })
    return results

# Function to test Hugging Face summarization with different lengths
def test_hf_summarization(text, lengths):
    hf_results = []
    for length in lengths:
        shortened_text = text[length]
        nlp_instance = NLP_Interface(text['original'])
        len_original = len(text['original'])
        len_shortened = len(text[length])
        percentage = min(len_shortened/len_original,1)
        summary = nlp_instance.summarization(percentage)
        hf_results.append({
            'ref_length': int(length),
            'text_length': len_original,
            'reference_length': len_shortened,
            'summary_length': len(summary),
            'percentage': percentage,
            'summary': summary,
            'reference': shortened_text
        })
    return hf_results

# Evaluate summary quality using ROUGE
def evaluate_summary_quality(reference, summary):
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
    scores = scorer.score(reference, summary)
    # Average the scores for ROUGE-1, ROUGE-2, and ROUGE-L
    average_score = (scores['rouge1'].fmeasure + scores['rouge2'].fmeasure + scores['rougeL'].fmeasure) / 3
    return average_score

# Test SpaCy with various text lengths and percentages
text_samples = [
    summaries['text1'], 
    summaries['text2'], 
    summaries['text3'],
    summaries['text4'], 
    summaries['text5'], 
    summaries['text6'],
    summaries['text7']
    ]
lengths = ["50", "100", "200", "300", "500", "1000"]

spacy_results = []
for text in text_samples:
    nlp_spacy = NLP_Interface(text['original'])
    spacy_results.extend(test_spacy_summarization(text, nlp_spacy, lengths))

# Record the SpaCy results
spacy_df = pd.DataFrame(spacy_results)
spacy_df.to_csv('spacy_results.csv', index=False)

# Test Hugging Face with various text lengths (percentage not applicable)
hf_results = []
for text in text_samples:
    hf_results.extend(test_hf_summarization(text, lengths))

# Record the Hugging Face results
hf_df = pd.DataFrame(hf_results)
hf_df.to_csv('huggingface_results.csv', index=False)


# Add quality scores to the dataframes
spacy_df['quality'] = spacy_df.apply(lambda row: evaluate_summary_quality(row['reference'], row['summary']), axis=1)
hf_df['quality'] = hf_df.apply(lambda row: evaluate_summary_quality(row['reference'], row['summary']), axis=1)

# Combine results for comparison
combined_df = pd.concat([spacy_df.assign(library='spacy'), hf_df.assign(library='huggingface')])
combined_df.to_csv('combined_results.csv', index=False)

