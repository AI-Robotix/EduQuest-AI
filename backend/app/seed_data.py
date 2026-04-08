USERS = [{'name': 'Maya',
  'email': 'maya@student.demo',
  'password_hash': '3688058a6965c4c8e143d7002afb557fe910657ad819714abb0356c7551c84b7',
  'role': 'student',
  'interests': 'python,machine learning,generative ai',
  'coins': 140,
  'level': 1,
  'streak': 2,
  'team_name': 'Team Aurora'},
 {'name': 'Leo',
  'email': 'leo@student.demo',
  'password_hash': '115f652493147e000824c52a7c6cb2cb776fbdbe8f67680832f00b21c315fe3d',
  'role': 'student',
  'interests': 'deep learning,python',
  'coins': 120,
  'level': 1,
  'streak': 1,
  'team_name': 'Team Aurora'},
 {'name': 'Dr. Rivera',
  'email': 'rivera@teacher.demo',
  'password_hash': 'cde383eee8ee7a4400adf7a15f716f179a2eb97646b37e089eb8d6d04e663416',
  'role': 'teacher',
  'interests': 'learning analytics,ai literacy',
  'coins': 0,
  'level': 1,
  'streak': 0,
  'team_name': None}]

COURSES = [{'title': 'Python Foundations',
  'slug': 'python-foundations',
  'category': 'Programming',
  'level': 'Beginner',
  'duration': '4 weeks',
  'description': 'Core Python syntax, loops, functions, and data structures for first-year STEM '
                 'students.',
  'learning_outcomes': 'Write simple Python programs, reason about loops and functions, and debug '
                       'basic scripts.',
  'lessons_json': '[{"title": "Week 1 \\u00b7 Variables and Types", "topic": "Python Basics", '
                  '"summary": "Understand variables, numbers, strings, and basic input/output.", '
                  '"content": "This lesson introduces Python syntax, variable assignment, strings, '
                  'integers, floats, and print/input. Learners practice reading values, converting '
                  'types, and predicting output from short scripts.", "key_points": ["Variables '
                  'store values for reuse.", "Strings and numbers behave differently.", "Type '
                  'conversion prevents many beginner bugs."], "activity": "Write a tiny script '
                  'that asks for a name and prints a formatted greeting."}, {"title": "Week 2 '
                  '\\u00b7 Loops and Conditions", "topic": "Loops", "summary": "Use for-loops, '
                  'while-loops, and conditional logic to control program flow.", "content": "This '
                  'lesson explains when to use for versus while loops, how indentation controls '
                  'blocks, and how conditions shape program flow. It also covers common mistakes '
                  'like infinite loops and misplaced indentation.", "key_points": ["A for-loop '
                  'iterates over a sequence.", "A while-loop repeats while a condition stays '
                  'true.", "Indentation defines the code block in Python."], "activity": "Build a '
                  'loop that prints each item in a list and labels numbers as even or odd."}, '
                  '{"title": "Week 3 \\u00b7 Functions", "topic": "Functions", "summary": "Define '
                  'reusable functions and pass arguments clearly.", "content": "This lesson shows '
                  'how to create reusable functions, choose parameters, return values, and keep '
                  'function behavior focused. It also highlights the difference between printing a '
                  'value and returning one.", "key_points": ["Functions improve reuse.", '
                  '"Parameters make functions flexible.", "return sends a value back to the '
                  'caller."], "activity": "Create a function that converts Celsius to Fahrenheit '
                  'and test it with three inputs."}]',
  'bonus_reward_code': 'python-bonus-lab',
  'bonus_reward_cost': 45,
  'bonus_module_title': 'Bonus Lab · Debugging a Student Script',
  'bonus_module_content': 'Unlock a guided debugging lab with a buggy loop, a missing indentation '
                          'block, and a function design task. The lab is intended as a coin-based '
                          'capstone activity.'},
 {'title': 'Machine Learning Essentials',
  'slug': 'machine-learning-essentials',
  'category': 'AI/ML',
  'level': 'Intermediate',
  'duration': '5 weeks',
  'description': 'Metrics, supervised learning, overfitting, and model evaluation with practical '
                 'examples.',
  'learning_outcomes': 'Interpret confusion matrices, explain train-test splits, and compare basic '
                       'ML models.',
  'lessons_json': '[{"title": "Week 1 \\u00b7 Learning Tasks", "topic": "Foundations", "summary": '
                  '"Differentiate classification, regression, and clustering.", "content": "The '
                  'lesson explains the three common ML task families and the kind of output each '
                  'one produces. It uses simple classroom examples such as pass/fail prediction, '
                  'house-price estimation, and grouping similar observations.", "key_points": '
                  '["Classification predicts labels.", "Regression predicts continuous values.", '
                  '"Clustering groups similar items without labels."], "activity": "Match five '
                  'example problems to classification, regression, or clustering."}, {"title": '
                  '"Week 2 \\u00b7 Metrics", "topic": "Metrics", "summary": "Compute precision, '
                  'recall, and accuracy from confusion matrices.", "content": "This lesson walks '
                  'through the confusion matrix and shows how accuracy, precision, and recall '
                  'answer different evaluation questions. It emphasizes that the right metric '
                  'depends on the error costs in the application.", "key_points": ["Accuracy '
                  'measures overall correctness.", "Precision focuses on predicted positives.", '
                  '"Recall focuses on actual positives that were found."], "activity": "Calculate '
                  'precision and recall for a small medical-screening example."}, {"title": "Week '
                  '3 \\u00b7 Generalization", "topic": "Generalization", "summary": "Explain '
                  'overfitting, underfitting, and train/validation/test splits.", "content": "The '
                  'lesson discusses how models can memorize training data, why validation matters, '
                  'and how train/validation/test splits support reliable evaluation. It also '
                  'introduces signs of overfitting in learning curves.", "key_points": '
                  '["Overfitting hurts performance on unseen data.", "Validation data helps tune '
                  'choices.", "Test data should stay untouched until final evaluation."], '
                  '"activity": "Interpret two short training curves and decide which one shows '
                  'overfitting."}]',
  'bonus_reward_code': 'ml-bonus-case-study',
  'bonus_reward_cost': 55,
  'bonus_module_title': 'Bonus Case Study · Model Selection Clinic',
  'bonus_module_content': 'Unlock a case-study challenge that asks the learner to choose between '
                          'two models using metrics, class balance, and error costs.'},
 {'title': 'Deep Learning Studio',
  'slug': 'deep-learning-studio',
  'category': 'AI/ML',
  'level': 'Intermediate',
  'duration': '5 weeks',
  'description': 'Neural-network foundations, hidden layers, activations, and optimization '
                 'concepts.',
  'learning_outcomes': 'Explain the role of layers, activations, and gradient-based training in '
                       'deep models.',
  'lessons_json': '[{"title": "Week 1 \\u00b7 Network Anatomy", "topic": "Architecture", '
                  '"summary": "Input layers, hidden layers, output layers, and learned '
                  'representations.", "content": "Learners see how information flows through a '
                  'neural network, why hidden layers exist, and how features become more abstract '
                  'across the network. The lesson compares shallow and deeper models on the same '
                  'task.", "key_points": ["Input layers receive features.", "Hidden layers '
                  'transform representations.", "Output layers produce the final prediction."], '
                  '"activity": "Sketch a simple three-layer network for image classification and '
                  'label each layer."}, {"title": "Week 2 \\u00b7 Activations", "topic": "Neural '
                  'Networks", "summary": "Why nonlinear activations matter for expressive '
                  'models.", "content": "This lesson explains why stacking linear layers is not '
                  'enough and how activations such as ReLU give the network expressive power. It '
                  'also introduces the idea of vanishing gradients at a conceptual level.", '
                  '"key_points": ["Nonlinearity increases model expressiveness.", "ReLU is common '
                  'because it is simple and effective.", "Activation choice affects training '
                  'dynamics."], "activity": "Compare a purely linear network with one using ReLU '
                  'on a toy decision boundary."}, {"title": "Week 3 \\u00b7 Optimization", '
                  '"topic": "Optimization", "summary": "Gradient descent, learning rate, and '
                  'training stability.", "content": "The lesson describes gradient descent as '
                  'repeated updates that reduce loss. It also covers the effect of the learning '
                  'rate and what unstable or diverging loss curves can indicate during training.", '
                  '"key_points": ["Gradient descent follows the negative gradient.", "Learning '
                  'rate controls step size.", "Too large a step can make training unstable."], '
                  '"activity": "Review three loss curves and decide which one suggests the '
                  'learning rate is too high."}]',
  'bonus_reward_code': 'dl-bonus-optimization-lab',
  'bonus_reward_cost': 55,
  'bonus_module_title': 'Bonus Lab · Optimization Troubleshooting',
  'bonus_module_content': 'Unlock an advanced troubleshooting lab on exploding gradients, unstable '
                          'loss curves, and learning-rate tuning decisions.'},
 {'title': 'Generative AI in Practice',
  'slug': 'generative-ai-practice',
  'category': 'AI Literacy',
  'level': 'Beginner',
  'duration': '3 weeks',
  'description': 'Prompting, verification, RAG, privacy, and responsible AI use in learning '
                 'workflows.',
  'learning_outcomes': 'Write grounded prompts, verify outputs, and explain why retrieval-grounded '
                       'systems matter.',
  'lessons_json': '[{"title": "Week 1 \\u00b7 Prompting for Study Support", "topic": "Prompting", '
                  '"summary": "Write precise prompts with constraints and output format.", '
                  '"content": "This lesson shows how better prompts include a task, context, '
                  'constraints, and an expected format. It compares vague prompts with stronger '
                  'prompts for studying lecture notes and asking for revision material.", '
                  '"key_points": ["Be explicit about the task.", "Provide the source or context.", '
                  '"Ask for a clear output format."], "activity": "Rewrite a vague study prompt '
                  'into a grounded prompt with constraints."}, {"title": "Week 2 \\u00b7 '
                  'Verification and Safety", "topic": "Responsible Use", "summary": "Verify '
                  'answers, inspect sources, and avoid over-trusting fluent output.", "content": '
                  '"Learners practice checking claims against course notes, spotting unsupported '
                  'answers, and deciding when a model should say it is uncertain. The lesson also '
                  'highlights privacy-preserving habits when handling learner data.", '
                  '"key_points": ["Fluent output can still be wrong.", "Verification should use '
                  'trusted material.", "Minimize personal data in AI workflows."], "activity": '
                  '"Judge three AI responses and identify which one is the safest to trust."}, '
                  '{"title": "Week 3 \\u00b7 Why RAG?", "topic": "RAG", "summary": "Use '
                  'retrieval-grounded systems to answer from approved course materials.", '
                  '"content": "This lesson explains retrieval-augmented generation as a way to '
                  'connect model answers to approved documents. Learners compare a generic chatbot '
                  'answer with a grounded answer that cites course materials.", "key_points": '
                  '["Retrieval adds relevant evidence.", "Grounded systems improve traceability.", '
                  '"Citations help learners verify answers."], "activity": "Compare two tutor '
                  'responses and justify which one is safer for teaching support."}]',
  'bonus_reward_code': 'genai-bonus-rag-clinic',
  'bonus_reward_cost': 50,
  'bonus_module_title': 'Bonus Clinic · Build a Safer Tutor',
  'bonus_module_content': 'Unlock a mini design clinic where the learner compares a generic '
                          'chatbot with a retrieval-grounded tutor and justifies safer deployment '
                          'choices.'}]

QUESTS = [{'title': 'Prompt Precision Starter',
  'track': 'AI Literacy',
  'skill_tag': 'prompting',
  'difficulty': 1,
  'description': 'Choose the most specific prompt for a study assistant.',
  'prompt': 'Which prompt is best if a student wants a grounded summary of lecture notes?\n'
            'A) Explain AI\n'
            'B) Summarize these lecture notes in 5 bullet points and cite the section titles used\n'
            'C) Tell me something interesting\n'
            'D) Make it fun',
  'question_type': 'mcq',
  'accepted_answers': 'b',
  'explanation': 'Prompt B is strongest because it specifies the task, format, source material, '
                 'and asks for grounded citations.',
  'badge_name': 'Prompt Starter',
  'reward_coins': 20,
  'hint': 'Choose the option that gives a clear task, source context, and output format.'},
 {'title': 'Hallucination Safety Check',
  'track': 'AI Literacy',
  'skill_tag': 'verification',
  'difficulty': 2,
  'description': 'Recognize a safe response to possible hallucinations.',
  'prompt': 'A chatbot gives a confident answer about a paper you have not read. Name one safe '
            'next step before you rely on the answer.',
  'question_type': 'contains_any',
  'accepted_answers': 'verify|check source|read source|cross-check|compare source|citation',
  'explanation': 'A safe next step is to verify the claim against the original source or a trusted '
                 'reference.',
  'badge_name': 'Verification Scout',
  'reward_coins': 25,
  'hint': 'The safest response admits uncertainty and checks an approved source.'},
 {'title': 'Privacy by Design',
  'track': 'Responsible AI',
  'skill_tag': 'privacy',
  'difficulty': 2,
  'description': 'Choose the safer handling of learner data.',
  'prompt': 'Which option is safer when preparing student data for an AI-supported learning tool?\n'
            'A) Upload full names and grades to any tool\n'
            'B) Minimize personal data and remove identifiers where possible\n'
            'C) Share everything because the model needs context\n'
            'D) Store passwords with the dataset',
  'question_type': 'mcq',
  'accepted_answers': 'b',
  'explanation': 'The safer approach is data minimization and removal of direct identifiers where '
                 'possible.',
  'badge_name': 'Privacy Guardian',
  'reward_coins': 20,
  'hint': 'Prefer data minimization and remove information that is not required.'},
 {'title': 'Why RAG?',
  'track': 'AI in Education',
  'skill_tag': 'rag_grounding',
  'difficulty': 3,
  'description': 'State the core benefit of retrieval-grounded tutors.',
  'prompt': 'Why is a retrieval-grounded tutor often safer for course support than a generic '
            'chatbot? Name one reason.',
  'question_type': 'contains_any',
  'accepted_answers': 'course materials|sources|citations|grounded|less '
                      'hallucination|evidence|retrieval',
  'explanation': 'A retrieval-grounded tutor can answer from course materials and show evidence, '
                 'which helps reduce unsupported answers.',
  'badge_name': 'Grounding Explorer',
  'reward_coins': 30,
  'hint': 'Think about what retrieval adds before generation starts.'},
 {'title': 'Micro Reflection',
  'track': 'Portfolio',
  'skill_tag': 'reflection',
  'difficulty': 1,
  'description': 'Practice evidence-based reflection.',
  'prompt': 'In one sentence, describe what makes a learning reflection useful.',
  'question_type': 'contains_any',
  'accepted_answers': 'evidence|example|specific|goal|improve|reflection',
  'explanation': 'Useful reflections are specific, evidence-based, and point to next steps for '
                 'improvement.',
  'badge_name': 'Reflective Learner',
  'reward_coins': 15,
  'hint': 'Include one thing you learned, one challenge, and one next step.'}]

QUIZZES = [{'course_slug': 'python-foundations',
  'title': 'Loop Logic',
  'topic': 'Loops',
  'skill_tag': 'python_loops',
  'difficulty': 1,
  'prompt': 'Which Python statement repeats a block of code for each item in a list?\n'
            'A) if\n'
            'B) for\n'
            'C) def\n'
            'D) return',
  'question_type': 'mcq',
  'accepted_answers': 'b',
  'options_json': '["A) if", "B) for", "C) def", "D) return"]',
  'explanation': 'A for loop iterates over items in a sequence.',
  'reward_coins': 12,
  'hint': 'Look for the Python keyword that iterates over items in a sequence.'},
 {'course_slug': 'python-foundations',
  'title': 'Mutable Structures',
  'topic': 'Lists',
  'skill_tag': 'python_lists',
  'difficulty': 2,
  'prompt': 'Name one property of a Python list.',
  'question_type': 'contains_any',
  'accepted_answers': 'mutable|ordered|index|append|list',
  'options_json': None,
  'explanation': 'Python lists are ordered, mutable collections that support indexing and '
                 'appending.',
  'reward_coins': 15,
  'hint': 'The correct data structure can be modified after creation.'},
 {'course_slug': 'machine-learning-essentials',
  'title': 'Precision Quiz',
  'topic': 'Metrics',
  'skill_tag': 'metrics_precision',
  'difficulty': 2,
  'prompt': 'For a classifier with TP=18, FP=6, what is precision? Enter a decimal.',
  'question_type': 'numeric',
  'accepted_answers': '0.75',
  'options_json': None,
  'explanation': 'Precision = TP / (TP + FP) = 18 / 24 = 0.75.',
  'reward_coins': 18,
  'hint': 'Precision asks: when the model predicted positive, how often was it correct?'},
 {'course_slug': 'machine-learning-essentials',
  'title': 'Overfitting Signal',
  'topic': 'Generalization',
  'skill_tag': 'generalization',
  'difficulty': 2,
  'prompt': 'What usually happens in overfitting?\n'
            'A) Both training and validation error decrease strongly\n'
            'B) Training performance is high but validation performance drops\n'
            'C) The model has no parameters\n'
            'D) Data is always balanced',
  'question_type': 'mcq',
  'accepted_answers': 'b',
  'options_json': '["A) Both training and validation error decrease strongly", "B) Training '
                  'performance is high but validation performance drops", "C) The model has no '
                  'parameters", "D) Data is always balanced"]',
  'explanation': 'Overfitting appears when a model fits the training data too closely and '
                 'generalizes poorly.',
  'reward_coins': 15,
  'hint': 'Compare training performance with performance on unseen data.'},
 {'course_slug': 'deep-learning-studio',
  'title': 'Hidden Layers',
  'topic': 'Architecture',
  'skill_tag': 'nn_layers',
  'difficulty': 2,
  'prompt': 'What is one role of hidden layers in a neural network?',
  'question_type': 'contains_any',
  'accepted_answers': 'features|representation|nonlinear|patterns|transform',
  'options_json': None,
  'explanation': 'Hidden layers learn internal representations and help model nonlinear patterns.',
  'reward_coins': 15,
  'hint': 'Hidden layers help the model learn intermediate patterns.'},
 {'course_slug': 'deep-learning-studio',
  'title': 'Gradient Direction',
  'topic': 'Optimization',
  'skill_tag': 'gradient_descent',
  'difficulty': 2,
  'prompt': 'In gradient descent, do we update parameters to increase or decrease the loss?',
  'question_type': 'contains_any',
  'accepted_answers': 'decrease|reduce|minimize|lower',
  'options_json': None,
  'explanation': 'Gradient descent updates parameters to reduce the loss function.',
  'reward_coins': 15,
  'hint': 'The update step should move parameters toward lower loss.'},
 {'course_slug': 'generative-ai-practice',
  'title': 'Grounded Prompting',
  'topic': 'Prompting',
  'skill_tag': 'prompting',
  'difficulty': 1,
  'prompt': 'Which instruction makes an LLM answer more grounded?\n'
            'A) Be creative\n'
            'B) Use the provided lecture notes and cite the section titles\n'
            'C) Answer quickly\n'
            'D) Avoid details',
  'question_type': 'mcq',
  'accepted_answers': 'b',
  'options_json': '["A) Be creative", "B) Use the provided lecture notes and cite the section '
                  'titles", "C) Answer quickly", "D) Avoid details"]',
  'explanation': 'Grounded prompting names the source material and often asks for traceable '
                 'evidence.',
  'reward_coins': 12,
  'hint': 'The better prompt includes task, context, constraints, and output format.'},
 {'course_slug': 'generative-ai-practice',
  'title': 'RAG Benefit',
  'topic': 'RAG',
  'skill_tag': 'rag_grounding',
  'difficulty': 2,
  'prompt': 'Name one reason why RAG is useful in educational support systems.',
  'question_type': 'contains_any',
  'accepted_answers': 'citations|evidence|course material|grounded|less hallucination|retrieval',
  'options_json': None,
  'explanation': 'RAG helps answers stay tied to approved materials and makes it easier to cite '
                 'evidence.',
  'reward_coins': 18,
  'hint': 'Retrieval lets the model answer from trusted material instead of memory alone.'}]

EXERCISES = [{'course_slug': 'python-foundations',
  'title': 'Write a Counting Loop',
  'topic': 'Loops',
  'skill_tag': 'python_loops',
  'difficulty': 2,
  'prompt': 'Write the missing keyword to complete this idea: ____ item in numbers:',
  'question_type': 'contains_any',
  'accepted_answers': 'for',
  'hint': 'Think about the keyword used for iteration in Python.',
  'solution': "The correct keyword is 'for', as in 'for item in numbers:'.",
  'reward_coins': 20},
 {'course_slug': 'python-foundations',
  'title': 'Function Basics',
  'topic': 'Functions',
  'skill_tag': 'python_functions',
  'difficulty': 2,
  'prompt': 'Which keyword is used to define a function in Python?',
  'question_type': 'contains_any',
  'accepted_answers': 'def',
  'hint': 'It is a three-letter keyword used before the function name.',
  'solution': "Use the keyword 'def', for example: def greet(name):",
  'reward_coins': 20},
 {'course_slug': 'machine-learning-essentials',
  'title': 'Compute Recall',
  'topic': 'Metrics',
  'skill_tag': 'metrics_recall',
  'difficulty': 3,
  'prompt': 'TP=24 and FN=6. Compute recall as a decimal.',
  'question_type': 'numeric',
  'accepted_answers': '0.8',
  'hint': 'Recall uses TP in the numerator and TP + FN in the denominator.',
  'solution': 'Recall = TP / (TP + FN) = 24 / 30 = 0.8.',
  'reward_coins': 25},
 {'course_slug': 'machine-learning-essentials',
  'title': 'Data Split Reflection',
  'topic': 'Evaluation',
  'skill_tag': 'train_test_split',
  'difficulty': 2,
  'prompt': 'Why do we keep a test set separate from the training set? Give one reason.',
  'question_type': 'contains_any',
  'accepted_answers': 'generalization|evaluation|unseen|test|overfitting|fair',
  'hint': 'Think about how we estimate performance on unseen data.',
  'solution': 'A test set provides an unbiased estimate of how well the model generalizes to '
              'unseen examples.',
  'reward_coins': 22},
 {'course_slug': 'deep-learning-studio',
  'title': 'Activation Purpose',
  'topic': 'Neural Networks',
  'skill_tag': 'activations',
  'difficulty': 2,
  'prompt': 'Why are activation functions important in neural networks? Give one reason.',
  'question_type': 'contains_any',
  'accepted_answers': 'nonlinear|non-linearity|complex patterns|decision boundary',
  'hint': 'Without activation functions, stacked layers behave too simply.',
  'solution': 'Activation functions introduce nonlinearity, allowing networks to model complex '
              'patterns.',
  'reward_coins': 24},
 {'course_slug': 'deep-learning-studio',
  'title': 'Learning Rate Judgment',
  'topic': 'Optimization',
  'skill_tag': 'learning_rate',
  'difficulty': 3,
  'prompt': 'What can happen if the learning rate is too high? Name one possible effect.',
  'question_type': 'contains_any',
  'accepted_answers': 'diverge|unstable|overshoot|oscillate|not converge',
  'hint': 'Think about the optimization steps moving too far each update.',
  'solution': 'If the learning rate is too high, optimization can overshoot minima and become '
              'unstable or diverge.',
  'reward_coins': 24},
 {'course_slug': 'generative-ai-practice',
  'title': 'Verification Routine',
  'topic': 'Responsible Use',
  'skill_tag': 'verification',
  'difficulty': 2,
  'prompt': 'Name one action you should take before citing an LLM answer in academic work.',
  'question_type': 'contains_any',
  'accepted_answers': 'verify|check source|cross-check|read original|citation',
  'hint': 'Think about evidence and source reliability.',
  'solution': 'Verify the claim against the original source or another trusted reference before '
              'citing it.',
  'reward_coins': 22},
 {'course_slug': 'generative-ai-practice',
  'title': 'Privacy Guardrail',
  'topic': 'Responsible Use',
  'skill_tag': 'privacy',
  'difficulty': 2,
  'prompt': 'What is one safe practice when using student data with AI tools?',
  'question_type': 'contains_any',
  'accepted_answers': 'minimize|remove identifiers|anonymize|privacy|consent',
  'hint': 'Focus on collecting only what is necessary and protecting identities.',
  'solution': 'Use data minimization and remove identifiers where possible before using AI tools.',
  'reward_coins': 22}]

COURSE_DOCUMENTS = [{'title': 'Python Loops Lecture Note',
  'source': 'Python Foundations - Week 1',
  'course_slug': 'python-foundations',
  'content': 'A for loop iterates over items in a sequence such as a list. Python lists are '
             'ordered and mutable, so you can append or update elements. Functions are defined '
             'with the def keyword.'},
 {'title': 'ML Metrics Lecture Note',
  'source': 'Machine Learning Essentials - Week 2',
  'course_slug': 'machine-learning-essentials',
  'content': 'Precision is TP divided by TP plus FP. Recall is TP divided by TP plus FN. A '
             'held-out test set helps estimate performance on unseen data and monitor '
             'generalization.'},
 {'title': 'Deep Learning Lecture Note',
  'source': 'Deep Learning Studio - Week 2',
  'course_slug': 'deep-learning-studio',
  'content': 'Hidden layers learn intermediate representations. Activation functions add '
             'nonlinearity so the network can model complex patterns. Gradient descent updates '
             'parameters to reduce the loss.'},
 {'title': 'Generative AI Lecture Note',
  'source': 'Generative AI in Practice - Week 1',
  'course_slug': 'generative-ai-practice',
  'content': 'Grounded prompts specify the task, constraints, and source material. '
             'Retrieval-augmented generation can retrieve course notes before answering, which '
             'helps reduce unsupported responses and enables citations. Sensitive student data '
             'should be minimized and de-identified where possible.'}]

TEAM_CHALLENGES = [{'title': 'Collaborative Prompt Clinic',
  'theme': 'Collaborative AI Literacy',
  'skill_tag': 'prompting',
  'difficulty': 2,
  'description': 'Work with your team to improve a weak study prompt into a grounded one.',
  'prompt': 'Draft one stronger study prompt that asks for a grounded summary of lecture notes and '
            'explains how your team improved it.',
  'accepted_answers': 'lecture notes|summary|cite|citations|context|constraints',
  'hint': 'Include the task, the source material, and the output format in your answer.',
  'explanation': 'A collaborative prompt revision should make the task explicit, mention the '
                 'source material, and define the output format clearly.',
  'badge_name': 'Collaboration Prompt Builder',
  'reward_coins': 35},
 {'title': 'Teacher-in-the-Loop Safety Review',
  'theme': 'Responsible AI',
  'skill_tag': 'verification',
  'difficulty': 3,
  'description': 'As a team, decide when a teacher should review an AI-supported answer before it '
                 'is shown to learners.',
  'prompt': 'Name one situation where a teacher should review an AI-generated answer before '
            'students use it, and briefly justify your choice.',
  'accepted_answers': 'high stakes|assessment|grading|uncertain|hallucination|unsupported|feedback',
  'hint': 'Think about cases where accuracy, fairness, or educational impact matter most.',
  'explanation': 'Teacher review is especially important for high-stakes feedback, assessment, or '
                 'any answer that may be unsupported or misleading.',
  'badge_name': 'Human Oversight Advocate',
  'reward_coins': 40},
 {'title': 'Shared RAG Design Sprint',
  'theme': 'AI in Education',
  'skill_tag': 'rag_grounding',
  'difficulty': 3,
  'description': 'Design a team proposal for a safer tutor grounded in course material.',
  'prompt': 'Give one reason why a retrieval-grounded tutor is safer for digital learning, and '
            'name one type of approved source it should use.',
  'accepted_answers': 'evidence|citations|course materials|lecture notes|approved '
                      'sources|documents|less hallucination',
  'hint': 'Mention both the safety benefit and the approved source materials.',
  'explanation': 'A grounded tutor is safer because it answers from approved course sources and '
                 'can surface evidence learners and teachers can verify.',
  'badge_name': 'Grounded Tutor Designer',
  'reward_coins': 40}]
