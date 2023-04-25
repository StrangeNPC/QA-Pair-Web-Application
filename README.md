# QuestionAnswerPairGenerator

This is a Django web application that generates question-answer pairs for a given context. It allows users to input a context and a number of questions they want to generate. The application then uses two different pre-trained models to generate the questions and answers respectively. Finally, it saves the generated question-answer pairs into an Excel file that users can download.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/158t4vH0NhNqv1InYGfkiKPJy1ATb8ltq)


![Alt Text](ReadmeImage1.jpg)

## Prerequisites

1. Clone the repository to your local machine.

```bash
git clone https://github.com/StrangeNPC/QA-Pair-Web-Application.git
```

2. Install required packages using the following command.

```bash
pip install -r requirements.txt
```
3. Run Django Server

```bash
python manage.py runserver
```
## Usage/Examples

1. Open your web browser and go to http://localhost:8000/.


2. Enter a context and the number of questions you want to generate.


3. Click on the "Generate" button.

4. Wait for the application to generate the question-answer pairs.

5. Download the generated pairs.


## Contributing

Contributions are welcome. Please create an issue or submit a pull request if you want to contribute to this project.



## License

[MIT](https://choosealicense.com/licenses/mit/)
