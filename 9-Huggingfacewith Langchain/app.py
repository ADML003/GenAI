import validators,streamlit as stimport validators,streamlit as st

import tracebackfrom langchain.prompts import PromptTemplate

from langchain.prompts import PromptTemplatefrom langchain_groq import ChatGroq

from langchain_groq import ChatGroqfrom langchain.chains.summarize import load_summarize_chain

from langchain.chains.summarize import load_summarize_chainfrom langchain_community.document_loaders import YoutubeLoader,UnstructuredURLLoader

from langchain_community.document_loaders import YoutubeLoader,UnstructuredURLLoaderfrom langchain_huggingface import HuggingFaceEndpoint, HuggingFacePipeline

from langchain_huggingface import HuggingFaceEndpoint, HuggingFacePipeline



## sstreamlit APP

## sstreamlit APPst.set_page_config(page_title="LangChain: Summarize Text From YT or Website", page_icon="🦜")

st.set_page_config(page_title="LangChain: Summarize Text From YT or Website", page_icon="🦜")st.title("🦜 LangChain: Summarize Text From YT or Website")

st.title("🦜 LangChain: Summarize Text From YT or Website")st.subheader('Summarize URL')

st.subheader('Summarize URL')





## Get the Groq API Key and url(YT or website)to be summarized

## Get the Groq API Key and url(YT or website)to be summarizedwith st.sidebar:

with st.sidebar:    hf_api_key=st.text_input("Huggingface API Token",value="",type="password")

    hf_api_key=st.text_input("Huggingface API Token",value="",type="password")

generic_url=st.text_input("URL",label_visibility="collapsed")

generic_url=st.text_input("URL",label_visibility="collapsed")

## Gemma Model Using Groq API

# Add some example URLs for testing##llm =ChatGroq(model="Gemma-7b-It", groq_api_key=groq_api_key)

st.markdown("**Test URLs:**")

col1, col2, col3 = st.columns(3)# Function to create LLM with fallback

with col1:@st.cache_resource

    if st.button("📰 Test News Article"):def create_llm(hf_api_key):

        st.session_state.test_url = "https://www.bbc.com/news"    repo_id = "mistralai/Mistral-7B-Instruct-v0.3"

with col2:    

    if st.button("📖 Test Wikipedia"):    try:

        st.session_state.test_url = "https://en.wikipedia.org/wiki/Artificial_intelligence"        # Try HuggingFace Endpoint first (API)

with col3:        llm = HuggingFaceEndpoint(

    if st.button("🎥 Test YouTube"):            repo_id=repo_id,

        st.session_state.test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"            max_new_tokens=150,

            temperature=0.7,

# Use test URL if set            token=hf_api_key

if 'test_url' in st.session_state:        )

    generic_url = st.session_state.test_url        # Test if it works

    st.info(f"Using test URL: {generic_url}")        test_response = llm.invoke("test")

    del st.session_state.test_url        st.info("✅ Using HuggingFace API Endpoint")

        return llm

## Gemma Model Using Groq API    except Exception as e:

##llm =ChatGroq(model="Gemma-7b-It", groq_api_key=groq_api_key)        st.warning(f"⚠️ API Endpoint failed ({str(e)[:50]}...), falling back to local pipeline")

        try:

# Function to create LLM with fallback            # Fallback to local pipeline

@st.cache_resource            llm = HuggingFacePipeline.from_model_id(

def create_llm(hf_api_key):                model_id="google/flan-t5-small",  # Smaller model for faster loading

    repo_id = "mistralai/Mistral-7B-Instruct-v0.3"                task="text2text-generation",

                    model_kwargs={"temperature": 0.7, "max_length": 150}

    try:            )

        # Try HuggingFace Endpoint first (API)            st.info("✅ Using Local HuggingFace Pipeline")

        llm = HuggingFaceEndpoint(            return llm

            repo_id=repo_id,        except Exception as e2:

            max_new_tokens=150,            st.error(f"❌ Both API and local pipeline failed: {str(e2)}")

            temperature=0.7,            return None

            token=hf_api_key

        )# Create LLM instance

        # Test if it worksif 'llm' not in st.session_state:

        test_response = llm.invoke("test")    st.session_state.llm = None

        st.info("✅ Using HuggingFace API Endpoint")

        return llmprompt_template="""

    except Exception as e:Provide a summary of the following content in 300 words:

        st.warning(f"⚠️ API Endpoint failed ({str(e)[:50]}...), falling back to local pipeline")Content:{text}

        try:

            # Fallback to local pipeline"""

            llm = HuggingFacePipeline.from_model_id(prompt=PromptTemplate(template=prompt_template,input_variables=["text"])

                model_id="google/flan-t5-small",  # Smaller model for faster loading

                task="text2text-generation",if st.button("Summarize the Content from YT or Website"):

                model_kwargs={"temperature": 0.7, "max_length": 150}    ## Validate all the inputs

            )    if not hf_api_key.strip() or not generic_url.strip():

            st.info("✅ Using Local HuggingFace Pipeline")        st.error("Please provide the information to get started")

            return llm    elif not validators.url(generic_url):

        except Exception as e2:        st.error("Please enter a valid Url. It can may be a YT video utl or website url")

            st.error(f"❌ Both API and local pipeline failed: {str(e2)}")

            return None    else:

        try:

# Create LLM instance            with st.spinner("Initializing LLM..."):

if 'llm' not in st.session_state:                # Create or get LLM

    st.session_state.llm = None                llm = create_llm(hf_api_key)

                if llm is None:

prompt_template="""                    st.error("Failed to initialize LLM. Please check your API key and try again.")

Provide a summary of the following content in 300 words:                    st.stop()

Content:{text}                

            with st.spinner("Loading content..."):

"""                ## loading the website or yt video data

prompt=PromptTemplate(template=prompt_template,input_variables=["text"])                if "youtube.com" in generic_url:

                    loader=YoutubeLoader.from_youtube_url(generic_url,add_video_info=True)

if st.button("Summarize the Content from YT or Website"):                else:

    ## Validate all the inputs                    loader=UnstructuredURLLoader(urls=[generic_url],ssl_verify=False,

    if not hf_api_key.strip() or not generic_url.strip():                                                 headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"})

        st.error("Please provide the information to get started")                docs=loader.load()

    elif not validators.url(generic_url):

        st.error("Please enter a valid Url. It can may be a YT video utl or website url")            with st.spinner("Generating summary..."):

                ## Chain For Summarization

    else:                chain=load_summarize_chain(llm,chain_type="stuff",prompt=prompt)

        try:                output_summary=chain.run(docs)

            with st.spinner("Initializing LLM..."):

                # Create or get LLM                st.success(output_summary)

                llm = create_llm(hf_api_key)        except Exception as e:

                if llm is None:            st.exception(f"Exception:{e}")

                    st.error("Failed to initialize LLM. Please check your API key and try again.")                    
                    st.stop()
                
            with st.spinner("Loading content..."):
                ## loading the website or yt video data
                if "youtube.com" in generic_url:
                    try:
                        loader=YoutubeLoader.from_youtube_url(generic_url,add_video_info=True)
                        docs=loader.load()
                    except Exception as yt_error:
                        st.error(f"❌ YouTube loading failed: {str(yt_error)}")
                        st.info("💡 Try using a different YouTube URL or check if the video is accessible")
                        st.stop()
                else:
                    try:
                        loader=UnstructuredURLLoader(
                            urls=[generic_url],
                            ssl_verify=False,
                            headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"}
                        )
                        docs=loader.load()
                    except Exception as url_error:
                        st.error(f"❌ Website loading failed: {str(url_error)}")
                        st.info("💡 Try a different URL or check if the website is accessible")
                        st.stop()

                if not docs:
                    st.error("❌ No content could be extracted from the URL")
                    st.stop()

            with st.spinner("Generating summary..."):
                ## Chain For Summarization
                chain=load_summarize_chain(llm,chain_type="stuff",prompt=prompt)
                output_summary=chain.run(docs)

                st.success(output_summary)
        except Exception as e:
            st.error(f"❌ Unexpected error: {str(e)}")
            st.info("💡 Please try a different URL or check your internet connection")
            
            # Show detailed error information in expander
            with st.expander("🔍 Detailed Error Information"):
                st.code(str(e))
                st.write("**Error Type:**", type(e).__name__)
                
                # Try to get more detailed error info
                error_details = traceback.format_exc()
                st.code(error_details)