# corpus-to-questions
Take corpus and generates mcq questions

## How to run

1. Create a virtual env -> 
  python -m venv env
  
2. once the env is created activate it -> 
  cd ./env/Scripts; ./activate; cd ../../

3. Once activated, install this package ( run the command ) -> 
  pip install git+https://github.com/boudinfl/pke.git

4. Once the above package is installed the run -> 
  pip install -r requirements.txt
 
5. Once all the requirements are installed then run -> python main.py

6. Then once the server starts -> 
  double click on index.html and use it

6. After 2-3 uses, comments line 2 and 3 inside the file summarizer_model_base_functions.py


## Extra info

There's one layer of cache on top of API abstraction. Means the first time the API will be slow but when the same file is uploaded second time, the API response will be JIT.
For demonstration try to have 3-4 text files saved locally and use them 2-3 times. The server will be ready to show
