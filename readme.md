# Local Network-Security Tutor & Quiz Bot (Privacy-Preserving)

##  Overview

This project aims to develop an offline-capable, intelligent tutoring system focused on **Network Security** education. It features two key AI agents:

- **Q&A Tutor Agent** – Answers user questions using a structured local knowledge base.
- **Quiz Agent** – Generates and grades practice questions (MCQs, T/F, and open-ended) with citation-backed feedback.

All functionality is designed for **privacy-aware**, **offline inference**, ensuring accessibility and security during usage.

---

##  Round 1 Development Goals

###  Objectives
- Build the **core system architecture**.
- Design and structure the **local knowledge base** from curated course materials.
- Develop both the **Q&A Tutor Agent** and the **Quiz Agent**.
- Implement **retrieval pipelines**, **question generation**, and **grading subsystems**.

###  Intelligent Agent Features

#### Q&A Tutor Agent:
- Embedding-based semantic search
- Keyword-matching retrieval
- Preprocessed knowledge base for fast lookups

#### Quiz Agent:
- Generates MCQs, true/false, and open-ended questions
- Provides reference answers with citations
- Grades user inputs and gives detailed feedback

---

##  Deliverables (Round 1)

-  Project Proposal
-  System Framework Design
-  Structured Local Knowledge Base
-  Preliminary Implementation of Tutor and Quiz Agents
-  Testing Documentation

---

## 🛠️ Tech Stack

- **Python 3.x**
- **NLTK / spaCy** – Text preprocessing
- **FAISS / SentenceTransformers** – Semantic search
- **scikit-learn / NumPy** – Support for grading logic
- **pytest** – Testing

---

##  Roadmap

### Future Enhancements:
- [ ] Improve embedding model for more accurate retrieval
- [ ] Implement advanced grading rubric with partial credit scoring
- [ ] Add user interaction interface (CLI or GUI)
- [ ] Enhance privacy with local model compression and encryption
- [ ] Conduct usability testing with real students

---

##  Testing

Functional tests will verify:
- Answer accuracy and citation validity (Tutor Agent)
- Question quality and answer coverage (Quiz Agent)
- Grading consistency using known inputs

## Contributors


| Name                              | R#        | Email                                       |
| --------------------------------- | --------- | ------------------------------------------- |
| **Brahmanya Asrit Sudulagunta**   | R11955267 | [bsudulag@ttu.edu](mailto:bsudulag@ttu.edu) |
| **Nithin Kumar Jada**             | R11969019 | [njada@ttu.edu](mailto:njada@ttu.edu)       |
| **Rakesh Ponugumati**             | R11965486 | [rponugum@ttu.edu](mailto:rponugum@ttu.edu) |
| **Venkata Sai Karthik Matha**     | R11944417 | [vmatha@ttu.edu](mailto:vmatha@ttu.edu)     |
| **Jatin Mallarapu**               | R11955268 | [jmallara@ttu.edu](mailto:jmallara@ttu.edu) |
| **Renuka Mantena**                | R11949084 | [remanten@ttu.edu](mailto:remanten@ttu.edu) |
| **Nikhil Chakravarthy Chappalli** | R11976478 | [nchappal@ttu.edu](mailto:nchappal@ttu.edu) |
| **Ramya Samala**                  | R11926730 | [ramsamal@ttu.edu](mailto:ramsamal@ttu.edu) |


