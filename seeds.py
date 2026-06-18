"""Seed data for the reading section.
All articles are genuinely free to access — no subscription required.
Run once on first boot (table is empty), or call seed_articles(db) to refresh.
"""

SEED_ARTICLES = [

    # ── HABITS & BEHAVIOUR ──────────────────────────────────────────────────

    {
        "title": "The Surprising Habits of Original Thinkers",
        "summary": (
            "Adam Grant explores what it means to be an original — someone who champions new ideas "
            "and acts on them. Originals are not fearless risk-takers; they are thoughtful doubters who "
            "procrastinate strategically and are motivated more by the fear of regret than failure."
        ),
        "url": "https://www.ted.com/talks/adam_grant_the_surprising_habits_of_original_thinkers",
        "author": "Adam Grant",
        "tags": "creativity, habits, psychology",
        "content_type": "TED Talk",
    },
    {
        "title": "Forget Big Change, Start with a Tiny Habit",
        "summary": (
            "Motivation is unreliable, but design is not. BJ Fogg explains why anchoring new behaviors "
            "to existing routines and celebrating tiny wins is far more effective than relying on willpower."
        ),
        "url": "https://www.youtube.com/watch?v=AdKUJxjn-R8",
        "author": "BJ Fogg",
        "tags": "habits, behaviour, psychology",
        "content_type": "Video Talk",
    },
    {
        "title": "How to Motivate Yourself to Change Your Behavior",
        "summary": (
            "The neuroscience of motivation reveals a counterintuitive truth: optimism and anticipated "
            "reward change behavior more reliably than fear. Sharot explains why nudges built around "
            "expectation and social norms outperform warning-based approaches."
        ),
        "url": "https://www.ted.com/talks/tali_sharot_how_to_motivate_yourself_to_change_your_behavior",
        "author": "Tali Sharot",
        "tags": "behaviour, psychology, habits",
        "content_type": "TED Talk",
    },
    {
        "title": "The Power of Believing That You Can Improve",
        "summary": (
            "Dweck shows that believing abilities can be developed — a growth mindset — "
            "fundamentally changes how people respond to setbacks, feedback, and challenge. "
            "This insight has reshaped education, coaching, and organizational psychology."
        ),
        "url": "https://www.ted.com/talks/carol_dweck_the_power_of_believing_that_you_can_improve",
        "author": "Carol Dweck",
        "tags": "psychology, habits, management",
        "content_type": "TED Talk",
    },
    {
        "title": "Atomic Habits: The Surprising Power of Tiny Gains",
        "summary": (
            "A 1% improvement every day compounds to a 37x gain over a year. Clear explains how "
            "small habits compound invisibly, why environment shapes behavior more than motivation, "
            "and why identity-based change outlasts willpower-based approaches."
        ),
        "url": "https://jamesclear.com/atomic-habits",
        "author": "James Clear",
        "tags": "habits, productivity, behaviour",
        "content_type": "Essay",
    },
    {
        "title": "How Long Does It Actually Take to Form a New Habit?",
        "summary": (
            "The popular 21-day habit myth is just that — a myth. UCL research found habit formation "
            "takes 18 to 254 days on average. Clear explains what actually drives the process and why "
            "missing one day does not derail long-term progress."
        ),
        "url": "https://jamesclear.com/new-habit",
        "author": "James Clear",
        "tags": "habits, behaviour, psychology",
        "content_type": "Blog Post",
    },
    {
        "title": "The Habit Loop: How Habits Work",
        "summary": (
            "Every habit follows a three-step loop: cue, routine, reward. Charles Duhigg shows how "
            "identifying the hidden cue and reward behind any unwanted habit is the master key to "
            "changing behavior. The same architecture that creates bad habits can build better ones."
        ),
        "url": "https://charlesduhigg.com/how-habits-work/",
        "author": "Charles Duhigg",
        "tags": "habits, behaviour, psychology",
        "content_type": "Blog Post",
    },
    {
        "title": "How to Make Stress Your Friend",
        "summary": (
            "For a decade, research suggested high stress was associated with elevated mortality — "
            "but only in people who believed stress was harmful. Those who viewed stress as the body "
            "preparing for challenge had some of the lowest mortality of any group studied."
        ),
        "url": "https://www.ted.com/talks/kelly_mcgonigal_how_to_make_stress_your_friend",
        "author": "Kelly McGonigal",
        "tags": "habits, psychology, wellbeing",
        "content_type": "TED Talk",
    },

    # ── PRODUCTIVITY & FOCUS ────────────────────────────────────────────────

    {
        "title": "The Ivy Lee Method: The Daily Routine Experts Recommend",
        "summary": (
            "In 1918 a consultant named Ivy Lee charged $25,000 for advice that fit on an index card: "
            "prioritize six tasks each night and work through them in order. Clear unpacks why it "
            "still outperforms sophisticated productivity systems a century later."
        ),
        "url": "https://jamesclear.com/ivy-lee",
        "author": "James Clear",
        "tags": "productivity, habits, management",
        "content_type": "Blog Post",
    },
    {
        "title": "How to Do Great Work",
        "summary": (
            "A long-form guide to producing the best work of your life. Graham argues that finding what "
            "you are naturally drawn to, pursuing it with curiosity, and pushing through the tedium of "
            "early stages is the formula shared by everyone who has done something truly original."
        ),
        "url": "https://paulgraham.com/greatwork.html",
        "author": "Paul Graham",
        "tags": "productivity, creativity, personal development",
        "content_type": "Essay",
    },
    {
        "title": "Maker's Schedule, Manager's Schedule",
        "summary": (
            "Managers thrive on one-hour slots; makers need uninterrupted half-day blocks. "
            "A single hour-long meeting can destroy an entire afternoon of creative output. "
            "This short essay is one of the most useful frameworks for understanding calendar conflicts."
        ),
        "url": "https://paulgraham.com/makersschedule.html",
        "author": "Paul Graham",
        "tags": "productivity, management, creativity",
        "content_type": "Essay",
    },
    {
        "title": "The Art of Saying No",
        "summary": (
            "Constraints force creativity. Farnam Street explores how the greatest thinkers guard their "
            "attention by ruthlessly declining good opportunities to pursue great ones — connecting "
            "Buffett, Jobs, and Munger to a single lesson: focus is the rarest form of clarity."
        ),
        "url": "https://fs.blog/saying-no/",
        "author": "Shane Parrish",
        "tags": "productivity, strategy, habits",
        "content_type": "Blog Post",
    },
    {
        "title": "Flow: The Secret to Happiness",
        "summary": (
            "Mihaly Csikszentmihalyi's framework of flow — complete absorption in a challenging, "
            "meaningful activity — explains why some hours feel deeply rewarding and others hollow. "
            "His TED talk distills 30 years of research on what makes an experience genuinely satisfying."
        ),
        "url": "https://www.ted.com/talks/mihaly_csikszentmihalyi_flow_the_secret_to_happiness",
        "author": "Mihaly Csikszentmihalyi",
        "tags": "productivity, psychology, wellbeing",
        "content_type": "TED Talk",
    },
    {
        "title": "Inside the Mind of a Master Procrastinator",
        "summary": (
            "Every procrastinator's brain contains an Instant Gratification Monkey who hijacks the "
            "Rational Decision-Maker whenever a task is not immediately fun. Tim Urban's viral TED talk "
            "reveals the hidden geography of the procrastinating mind — and introduces the Panic Monster."
        ),
        "url": "https://www.ted.com/talks/tim_urban_inside_the_mind_of_a_master_procrastinator",
        "author": "Tim Urban",
        "tags": "productivity, psychology, habits",
        "content_type": "TED Talk",
    },
    {
        "title": "Quit Social Media",
        "summary": (
            "Newport argues social media fragments attention, displaces deep work, and offers shallow "
            "substitutes for real-world accomplishment. This provocative TEDx talk makes the case for "
            "opting out — especially for professionals who rely on sustained cognitive performance."
        ),
        "url": "https://www.youtube.com/watch?v=3E7hkPZ-HTk",
        "author": "Cal Newport",
        "tags": "productivity, focus, technology",
        "content_type": "Video Talk",
    },
    {
        "title": "Deep Work: A Framework for Intense Focused Success",
        "summary": (
            "The ability to focus without distraction is becoming simultaneously rare and more valuable. "
            "Newport's core claim: those who develop capacity for deep work will thrive in the knowledge "
            "economy; those who cannot will be left behind."
        ),
        "url": "https://www.calnewport.com/blog/2015/10/22/deep-work-a-framework-for-intense-focused-success/",
        "author": "Cal Newport",
        "tags": "productivity, focus, habits",
        "content_type": "Blog Post",
    },
    {
        "title": "Why You Should Stop Caring What Other People Think",
        "summary": (
            "The social survival mammoth — our deep fear of other people's opinions — hijacks "
            "rational decision-making more than almost any other force. Tim Urban maps the hidden "
            "software running human social behavior and explains why dismantling it is essential "
            "for work that actually matters."
        ),
        "url": "https://waitbutwhy.com/2014/06/taming-mammoth-let-peoples-opinions-run-life.html",
        "author": "Tim Urban",
        "tags": "psychology, productivity, personal development",
        "content_type": "Blog Post",
    },
    {
        "title": "The Feynman Technique: The Best Way to Learn Anything",
        "summary": (
            "Nobel laureate Feynman believed you truly understand a concept only when you can explain "
            "it to a child. Clear breaks down the four-step Feynman Technique and shows why the act of "
            "explaining forces you to confront exactly the limits of your own understanding."
        ),
        "url": "https://jamesclear.com/feynman-technique",
        "author": "James Clear",
        "tags": "learning, productivity, education",
        "content_type": "Blog Post",
    },

    # ── LEADERSHIP & MANAGEMENT ─────────────────────────────────────────────

    {
        "title": "How Great Leaders Inspire Action",
        "summary": (
            "Great leaders start with why, not what. Sinek's Golden Circle explains why some leaders "
            "inspire loyalty while others, with comparable resources and talent, simply cannot."
        ),
        "url": "https://www.ted.com/talks/simon_sinek_how_great_leaders_inspire_action",
        "author": "Simon Sinek",
        "tags": "leadership, management, behaviour",
        "content_type": "TED Talk",
    },
    {
        "title": "Building a Psychologically Safe Workplace",
        "summary": (
            "Psychological safety — the belief you will not be punished for speaking up — is the "
            "single best predictor of team performance, outranking talent, resources, and strategy. "
            "Edmondson explains how leaders create conditions for candor in high-stakes environments."
        ),
        "url": "https://www.ted.com/talks/amy_edmondson_building_a_psychologically_safe_workplace",
        "author": "Amy Edmondson",
        "tags": "management, teams, leadership",
        "content_type": "TED Talk",
    },
    {
        "title": "How to Turn a Group of Strangers into a Team",
        "summary": (
            "Teaming — collaborating with new people on the fly — is increasingly essential as "
            "organizations become more fluid. Edmondson shares the conditions that allow diverse "
            "strangers to work effectively together without the luxury of time to build trust."
        ),
        "url": "https://www.ted.com/talks/amy_edmondson_how_to_turn_a_group_of_strangers_into_a_team",
        "author": "Amy Edmondson",
        "tags": "teams, management, leadership",
        "content_type": "TED Talk",
    },
    {
        "title": "The Puzzle of Motivation",
        "summary": (
            "Traditional carrot-and-stick motivation works for mechanical tasks but is counterproductive "
            "for creative, cognitive work. Pink argues that autonomy, mastery, and purpose are the true "
            "drivers of high performance — and most organizations ignore all three."
        ),
        "url": "https://www.ted.com/talks/dan_pink_the_puzzle_of_motivation",
        "author": "Daniel Pink",
        "tags": "management, psychology, behaviour",
        "content_type": "TED Talk",
    },
    {
        "title": "Keep Your Identity Small",
        "summary": (
            "The more central an idea is to your self-image, the less clearly you can think about it. "
            "Graham explains why attaching your identity to political, religious, or professional labels "
            "narrows thinking — and why the most intellectually honest people keep their identities lean."
        ),
        "url": "https://paulgraham.com/identity.html",
        "author": "Paul Graham",
        "tags": "leadership, psychology, personal development",
        "content_type": "Essay",
    },
    {
        "title": "First, Know Thyself",
        "summary": (
            "Leaders who lack self-awareness misread how others experience them, surround themselves "
            "with yes-men, and conflate confidence with competence. Farnam Street synthesizes research "
            "on why self-knowledge is the meta-skill that makes every other leadership capability possible."
        ),
        "url": "https://fs.blog/self-awareness/",
        "author": "Shane Parrish",
        "tags": "leadership, psychology, personal development",
        "content_type": "Blog Post",
    },
    {
        "title": "The Decision Matrix: How to Prioritize When Everything Feels Urgent",
        "summary": (
            "Eisenhower's urgent/important matrix remains one of the most practical leadership tools "
            "ever devised. Farnam Street explains why the biggest leadership error is spending all time "
            "in urgent/important work while neglecting the compounding returns of not-urgent/important."
        ),
        "url": "https://fs.blog/eisenhower-matrix/",
        "author": "Shane Parrish",
        "tags": "leadership, productivity, decision-making",
        "content_type": "Blog Post",
    },
    {
        "title": "What Makes Someone a Great Leader?",
        "summary": (
            "Goleman's foundational research established that emotional intelligence — self-awareness, "
            "empathy, self-regulation — predicts leadership effectiveness better than IQ or technical "
            "skill. This lecture walks through the five components and explains how they can be cultivated."
        ),
        "url": "https://www.youtube.com/watch?v=YiDcCVdKYEw",
        "author": "Daniel Goleman",
        "tags": "leadership, psychology, management",
        "content_type": "Video Talk",
    },
    {
        "title": "Gratitude Makes You a Better Leader",
        "summary": (
            "Leaders who regularly express genuine gratitude create psychological safety, higher retention, "
            "and better performance. Berkeley's Greater Good Science Center summarizes the organizational "
            "science of gratitude with actionable practices for leaders at every level."
        ),
        "url": "https://greatergood.berkeley.edu/article/item/gratitude_makes_you_a_better_leader",
        "author": "Greater Good Science Center",
        "tags": "leadership, wellbeing, management",
        "content_type": "Blog Post",
    },
    {
        "title": "The Multiplier Effect: Amplifying Intelligence Around You",
        "summary": (
            "Some leaders drain the intelligence of the people around them; others amplify it. "
            "Wiseman's research identifies the specific behaviors that distinguish Multipliers — who get "
            "twice the capability from their teams — from Diminishers who cause harm without realizing it."
        ),
        "url": "https://hbr.org/2010/05/bringing-out-the-best-in-your-people",
        "author": "Liz Wiseman",
        "tags": "leadership, management, teams",
        "content_type": "Magazine Article",
    },
    {
        "title": "What Is Evidence-Based Management?",
        "summary": (
            "Pfeffer and Sutton argue that management practice lags management research by decades — "
            "much as clinical practice once lagged clinical research. Their call applies the scientific "
            "skepticism of evidence-based medicine to hiring, incentive design, and organizational structure."
        ),
        "url": "https://hbr.org/2006/01/evidence-based-management",
        "author": "Jeffrey Pfeffer & Robert Sutton",
        "tags": "management, strategy, decision-making",
        "content_type": "Magazine Article",
    },
    {
        "title": "Tribal Leadership",
        "summary": (
            "Organizations can be mapped across five tribal stages. Logan's research on 24,000 people "
            "shows that leaders who understand which stage their team is in — and how to nudge it "
            "one level higher — consistently outperform those who ignore culture as a performance driver."
        ),
        "url": "https://www.ted.com/talks/david_logan_tribal_leadership",
        "author": "David Logan",
        "tags": "leadership, teams, management",
        "content_type": "TED Talk",
    },

    # ── MEDICINE & HEALTHCARE ───────────────────────────────────────────────

    {
        "title": "The Checklist",
        "summary": (
            "A simple, humble instrument — the checklist — has saved thousands of lives in aviation, "
            "construction, and medicine. Gawande explores how a two-minute pre-surgical checklist "
            "slashes complications, and why professional pride stands in the way of adopting it."
        ),
        "url": "https://www.newyorker.com/magazine/2007/12/10/the-checklist",
        "author": "Atul Gawande",
        "tags": "medicine, management, systems",
        "content_type": "Magazine Article",
    },
    {
        "title": "Slow Ideas",
        "summary": (
            "Why do some life-saving innovations spread in years while others take decades? Gawande "
            "contrasts the rapid adoption of anesthesia with the slow uptake of antiseptic technique, "
            "arguing that genuine behavior change requires human connection, not just better evidence."
        ),
        "url": "https://www.newyorker.com/magazine/2013/07/29/slow-ideas",
        "author": "Atul Gawande",
        "tags": "medicine, behaviour, change",
        "content_type": "Magazine Article",
    },
    {
        "title": "Personal Best",
        "summary": (
            "Top athletes and musicians take coaching for granted — so why do not doctors? Gawande "
            "asks what it would mean for physicians to have a trusted observer, and argues this may be "
            "the single most underused tool for sustained professional development."
        ),
        "url": "https://www.newyorker.com/magazine/2011/10/03/personal-best",
        "author": "Atul Gawande",
        "tags": "medicine, coaching, management",
        "content_type": "Magazine Article",
    },
    {
        "title": "A Doctor's Touch",
        "summary": (
            "The ritual of the physical exam is disappearing from medicine, replaced by data and screens. "
            "Verghese makes a passionate case that the ceremony of the bedside encounter is not "
            "inefficiency but meaning, and that patients need to be seen as people."
        ),
        "url": "https://www.ted.com/talks/abraham_verghese_a_doctor_s_touch",
        "author": "Abraham Verghese",
        "tags": "medicine, behaviour, leadership",
        "content_type": "TED Talk",
    },
    {
        "title": "What Doctors Don't Know About the Drugs They Prescribe",
        "summary": (
            "Almost half of clinical trial data is never published, and negative results are more likely "
            "to go unpublished than positive ones. Goldacre's TED talk on publication bias is one of "
            "the most important pieces of medical epistemology available in a public forum."
        ),
        "url": "https://www.ted.com/talks/ben_goldacre_what_doctors_don_t_know_about_the_drugs_they_prescribe",
        "author": "Ben Goldacre",
        "tags": "medicine, decision-making, systems",
        "content_type": "TED Talk",
    },
    {
        "title": "How Childhood Trauma Affects Health Across a Lifetime",
        "summary": (
            "Pediatrician Nadine Burke Harris explains the biology of toxic stress — how childhood "
            "adversity rewires the stress response in ways that increase heart disease and diabetes "
            "decades later. Her talk introduces the ACE score and makes the case for trauma-informed care."
        ),
        "url": "https://www.ted.com/talks/nadine_burke_harris_how_childhood_trauma_affects_health_across_a_lifetime",
        "author": "Nadine Burke Harris",
        "tags": "medicine, psychology, wellbeing",
        "content_type": "TED Talk",
    },
    {
        "title": "The Case for Rethinking How We Die",
        "summary": (
            "ICU physician Peter Saul challenges two assumptions dominating end-of-life care: that patients "
            "want maximal intervention, and that medicine has the right answers to existential questions. "
            "A talk about starting with the simplest question — what does a good death look like to you?"
        ),
        "url": "https://www.ted.com/talks/peter_saul_let_s_talk_about_dying",
        "author": "Peter Saul",
        "tags": "medicine, communication, wellbeing",
        "content_type": "TED Talk",
    },
    {
        "title": "How Doctors Think: Jerome Groopman",
        "summary": (
            "Groopman documents the systematic cognitive errors physicians make: premature closure, "
            "anchoring, and commission bias. His Google lecture is one of the best available resources "
            "on clinical reasoning for practicing physicians who want to reduce diagnostic error."
        ),
        "url": "https://www.youtube.com/watch?v=0Kk-9iCEMlQ",
        "author": "Jerome Groopman",
        "tags": "medicine, decision-making, psychology",
        "content_type": "Video Talk",
    },
    {
        "title": "Physician Burnout: Its Origin, Symptoms and Five Main Causes",
        "summary": (
            "Burnout is fundamentally different from stress — it is depersonalization combined with "
            "emotional exhaustion. This open-access PMC article covers the five systemic drivers and "
            "explains why individual wellness programs consistently fail to address root causes."
        ),
        "url": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7587270/",
        "author": "Liselotte Dyrbye et al.",
        "tags": "medicine, wellbeing, systems",
        "content_type": "Journal Article",
    },
    {
        "title": "The Myth of Average Applied to Clinical Protocols",
        "summary": (
            "The U.S. Air Force designed cockpits around the average pilot — and crashes increased. "
            "Todd Rose's TEDx talk explains that the average person does not exist and that designing "
            "for the average means designing for nobody. Direct implications for dosing and clinical protocols."
        ),
        "url": "https://www.youtube.com/watch?v=4eBmyttcfU4",
        "author": "Todd Rose",
        "tags": "medicine, systems, learning",
        "content_type": "Video Talk",
    },
    {
        "title": "What Recovery Teaches Us About the Brain",
        "summary": (
            "Jill Bolte Taylor watched her own brain fail hemisphere by hemisphere during a stroke and "
            "kept observing. Her TED talk is one of the most powerful ever given — and one of the best "
            "illustrations of what neuroplasticity and recovery feel like from the inside."
        ),
        "url": "https://www.ted.com/talks/jill_bolte_taylor_my_stroke_of_insight",
        "author": "Jill Bolte Taylor",
        "tags": "medicine, psychology, wellbeing",
        "content_type": "TED Talk",
    },
    {
        "title": "The Mathematics of Weight Loss",
        "summary": (
            "The 500-calorie deficit formula is provably wrong — it ignores metabolic adaptation. "
            "Ruben Meerman's viral TEDx talk explains the actual biochemistry of fat loss and answers "
            "the question most doctors cannot: where does fat actually go when you lose it?"
        ),
        "url": "https://www.ted.com/talks/ruben_meerman_the_mathematics_of_weight_loss",
        "author": "Ruben Meerman",
        "tags": "medicine, wellbeing, habits",
        "content_type": "TED Talk",
    },
    {
        "title": "Why Doctors Should Give Away Their Knowledge for Free",
        "summary": (
            "The traditional paywalled journal model is incompatible with evidence-based medicine's "
            "core commitments. Krumholz's TEDx Yale Medical School talk argues that open data and "
            "open access are prerequisites for the next phase of clinical improvement."
        ),
        "url": "https://www.youtube.com/watch?v=Q9fN8T4JVUI",
        "author": "Harlan Krumholz",
        "tags": "medicine, technology, systems",
        "content_type": "Video Talk",
    },
    {
        "title": "The Promise and Peril of AI in Medicine",
        "summary": (
            "Eric Topol's NEJM Perspective examines where AI has already outperformed human clinicians "
            "(diabetic retinopathy, ECG reading, dermatology), where it has not, and what the field needs "
            "to get right before widespread deployment changes the physician-patient relationship."
        ),
        "url": "https://www.nejm.org/doi/full/10.1056/NEJMra1814259",
        "author": "Eric Topol",
        "tags": "technology, medicine, decision-making",
        "content_type": "Journal Article",
    },
    {
        "title": "Medical Gaslighting: When Doctors Dismiss Patients' Symptoms",
        "summary": (
            "Medical gaslighting disproportionately affects women, people of color, and patients with "
            "medically unexplained conditions. The Conversation covers the diagnostic and trust "
            "consequences and proposes structural changes to clinical education that address it."
        ),
        "url": "https://theconversation.com/medical-gaslighting-when-health-care-providers-dismiss-your-symptoms-172193",
        "author": "The Conversation",
        "tags": "medicine, communication, psychology",
        "content_type": "Magazine Article",
    },

    # ── PSYCHOLOGY & DECISION-MAKING ────────────────────────────────────────

    {
        "title": "The Power of Vulnerability",
        "summary": (
            "Brene Brown argues that vulnerability is not weakness but the birthplace of creativity, "
            "connection, and joy. Her research on shame upends the idea that emotional exposure "
            "should be minimized — especially in leadership."
        ),
        "url": "https://www.ted.com/talks/brene_brown_the_power_of_vulnerability",
        "author": "Brene Brown",
        "tags": "psychology, leadership, vulnerability",
        "content_type": "TED Talk",
    },
    {
        "title": "Listening to Shame",
        "summary": (
            "Brown distinguishes shame — the fear of being unlovable — from guilt. She argues that "
            "empathy, not judgment, is the antidote, and that leaders who can sit with discomfort "
            "are the ones who build lasting trust."
        ),
        "url": "https://www.ted.com/talks/brene_brown_listening_to_shame",
        "author": "Brene Brown",
        "tags": "psychology, leadership, medicine",
        "content_type": "TED Talk",
    },
    {
        "title": "The New Era of Positive Psychology",
        "summary": (
            "Seligman reframes psychology around flourishing: positive emotion, engagement, relationships, "
            "meaning, and accomplishment. The discipline's traditional focus on pathology left out "
            "the question of what makes life worth living."
        ),
        "url": "https://www.ted.com/talks/martin_seligman_the_new_era_of_positive_psychology",
        "author": "Martin Seligman",
        "tags": "psychology, wellbeing, medicine",
        "content_type": "TED Talk",
    },
    {
        "title": "The Making of Behavioral Economics",
        "summary": (
            "Small, cheap changes to how choices are presented — defaults, framing, sequencing — reliably "
            "shift behavior without restricting freedom. Nobel laureate Thaler explains the architecture "
            "of choice and why nudge theory has been embraced by hospitals and governments."
        ),
        "url": "https://www.newyorker.com/magazine/2016/10/17/the-making-of-behavioral-economics",
        "author": "Richard Thaler",
        "tags": "behaviour, decision-making, psychology",
        "content_type": "Magazine Article",
    },
    {
        "title": "The Case Against Empathy",
        "summary": (
            "Empathy has a dark side: it is innumerate, parochial, and easily hijacked by vivid stories. "
            "Bloom argues that rational compassion — caring without losing perspective — produces better "
            "moral and clinical decisions than emotional empathy."
        ),
        "url": "https://www.theatlantic.com/science/archive/2015/09/the-violence-of-empathy/407155/",
        "author": "Paul Bloom",
        "tags": "psychology, medicine, decision-making",
        "content_type": "Magazine Article",
    },
    {
        "title": "Thinking Fast and Slow: Kahneman on Two Systems",
        "summary": (
            "System 1 is fast, intuitive, and emotional; System 2 is slow, deliberate, and logical. "
            "Kahneman's Big Think interview explains the interplay between the two systems and why "
            "System 1 makes predictable errors with real implications for medicine, law, and policy."
        ),
        "url": "https://www.youtube.com/watch?v=PirFrDVRBo4",
        "author": "Daniel Kahneman",
        "tags": "psychology, decision-making, behaviour",
        "content_type": "Video Talk",
    },
    {
        "title": "First Principles: The Building Blocks of True Knowledge",
        "summary": (
            "First-principles thinking — breaking a problem to its fundamental truths and rebuilding "
            "from there — is the cognitive style Musk associates with his most unconventional decisions. "
            "Farnam Street explains the concept and its Socratic origins."
        ),
        "url": "https://fs.blog/first-principles/",
        "author": "Shane Parrish",
        "tags": "decision-making, strategy, psychology",
        "content_type": "Blog Post",
    },
    {
        "title": "Inversion: The Power of Avoiding Stupidity",
        "summary": (
            "Charlie Munger: Invert, always invert. Instead of asking how to succeed, ask how to avoid "
            "failure. Inversion exposes hidden risks that forward-thinking misses — in medicine, "
            "investment, and organizational strategy."
        ),
        "url": "https://fs.blog/inversion/",
        "author": "Shane Parrish",
        "tags": "decision-making, strategy, psychology",
        "content_type": "Blog Post",
    },
    {
        "title": "The Psychology of Your Future Self",
        "summary": (
            "Humans dramatically underestimate how much they will change over the next decade — "
            "the end of history illusion. Dan Gilbert's research has enormous implications for medical "
            "decision-making, retirement planning, and career development."
        ),
        "url": "https://www.ted.com/talks/dan_gilbert_the_psychology_of_your_future_self",
        "author": "Dan Gilbert",
        "tags": "psychology, decision-making, wellbeing",
        "content_type": "TED Talk",
    },
    {
        "title": "Thinking in Bets: Good Decisions vs. Good Outcomes",
        "summary": (
            "Good decisions can lead to bad outcomes, and vice versa. Former poker pro Annie Duke "
            "explains why outcome bias — judging a decision by its result — is the biggest impediment "
            "to learning. Her framework applies directly to clinical and managerial choices."
        ),
        "url": "https://www.youtube.com/watch?v=OaO5LbHWuYg",
        "author": "Annie Duke",
        "tags": "decision-making, strategy, psychology",
        "content_type": "Video Talk",
    },
    {
        "title": "Are We in Control of Our Own Decisions?",
        "summary": (
            "Context — default options, ordering, decoy alternatives — determines decisions far more "
            "than preferences do. Ariely's TED talk on choice architecture shows why default organ "
            "donation consent is a public health intervention as powerful as any information campaign."
        ),
        "url": "https://www.ted.com/talks/dan_ariely_are_we_in_control_of_our_own_decisions",
        "author": "Dan Ariely",
        "tags": "behaviour, decision-making, medicine",
        "content_type": "TED Talk",
    },

    # ── WELLBEING & MENTAL HEALTH ───────────────────────────────────────────

    {
        "title": "The Happy Secret to Better Work",
        "summary": (
            "A positive brain is 31% more productive, more creative, and more resilient. Achor's "
            "research-backed TED talk delivers seven practical interventions with a combined effect "
            "size larger than most antidepressant trials in the literature."
        ),
        "url": "https://www.ted.com/talks/shawn_achor_the_happy_secret_to_better_work",
        "author": "Shawn Achor",
        "tags": "wellbeing, psychology, productivity",
        "content_type": "TED Talk",
    },
    {
        "title": "What Makes a Good Life? Lessons from the Longest Study on Happiness",
        "summary": (
            "The Harvard Study of Adult Development tracked 724 men for 75 years. The conclusion: it "
            "was not fame, wealth, or achievement that predicted healthy aging — it was the quality "
            "of relationships. Robert Waldinger presents the evidence in this landmark TED talk."
        ),
        "url": "https://www.ted.com/talks/robert_waldinger_what_makes_a_good_life_lessons_from_the_longest_study_on_happiness",
        "author": "Robert Waldinger",
        "tags": "wellbeing, psychology, medicine",
        "content_type": "TED Talk",
    },
    {
        "title": "Sleep Is Your Superpower",
        "summary": (
            "When the US moves to daylight saving time and loses one hour of sleep, hospital admissions "
            "for heart attacks jump 24% the next day. Walker's TED talk on the biology of sleep and "
            "the devastating health effects of deprivation is one of the most practically important talks available."
        ),
        "url": "https://www.ted.com/talks/matt_walker_sleep_is_your_superpower",
        "author": "Matthew Walker",
        "tags": "wellbeing, medicine, habits",
        "content_type": "TED Talk",
    },
    {
        "title": "The Power of Mindfulness",
        "summary": (
            "Mindfulness is not about emptying the mind — it is about practicing kind attention. "
            "Neuroscience shows that regular practice restructures the brain's default mode network, "
            "reducing rumination and increasing attentional control in any high-stress environment."
        ),
        "url": "https://www.ted.com/talks/shauna_shapiro_the_power_of_mindfulness_what_you_practice_grows_stronger",
        "author": "Shauna Shapiro",
        "tags": "wellbeing, psychology, habits",
        "content_type": "TED Talk",
    },
    {
        "title": "Everything You Know About Addiction Is Wrong",
        "summary": (
            "Johann Hari spent three years researching the real causes of addiction. His TED talk "
            "overturns the dominant model — that addiction is caused by chemical hooks — in favor of "
            "a connection-based theory with profound implications for clinical treatment and social policy."
        ),
        "url": "https://www.ted.com/talks/johann_hari_everything_you_think_you_know_about_addiction_is_wrong",
        "author": "Johann Hari",
        "tags": "medicine, psychology, wellbeing",
        "content_type": "TED Talk",
    },
    {
        "title": "The Self-Compassion Edge",
        "summary": (
            "Kristin Neff's research shows self-compassion outperforms self-esteem as a predictor of "
            "wellbeing, motivation, and resilience — partly because self-esteem requires external "
            "validation while self-compassion is internally stable. Critical insight for high-achieving "
            "professionals prone to harsh self-judgment."
        ),
        "url": "https://www.ted.com/talks/kristin_neff_the_space_between_self_esteem_and_humility",
        "author": "Kristin Neff",
        "tags": "wellbeing, psychology, personal development",
        "content_type": "TED Talk",
    },
    {
        "title": "Burnout and How to Complete the Stress Cycle",
        "summary": (
            "Stuck stress — the physiological residue of incomplete stress responses — makes exercise "
            "feel impossible when you most need it. Emily and Amelia Nagoski explain the biology of "
            "burnout and what actually completes the stress cycle."
        ),
        "url": "https://www.ted.com/talks/emily_nagoski_and_amelia_nagoski_burnout_and_how_to_complete_the_stress_cycle",
        "author": "Emily & Amelia Nagoski",
        "tags": "wellbeing, medicine, habits",
        "content_type": "TED Talk",
    },
    {
        "title": "The Science of Gratitude and Why It Matters for Health",
        "summary": (
            "A gratitude practice — writing three specific things you are grateful for — has a "
            "measurable and robust effect on wellbeing, immune function, and social relationships. "
            "The Conversation summarizes 20 years of randomized controlled trials."
        ),
        "url": "https://theconversation.com/the-science-of-gratitude-and-how-it-can-improve-your-health-and-wellbeing-172753",
        "author": "The Conversation",
        "tags": "wellbeing, medicine, habits",
        "content_type": "Magazine Article",
    },
    {
        "title": "Exercise as Medicine",
        "summary": (
            "A 30-minute moderate-intensity walk five days a week reduces all-cause mortality more "
            "than statins for most people without known cardiovascular disease — yet fewer than 20% "
            "of physicians regularly prescribe exercise. This BMJ Open review makes the case for change."
        ),
        "url": "https://bmjopen.bmj.com/content/9/9/e033131",
        "author": "Edwards & Loprinzi",
        "tags": "medicine, wellbeing, habits",
        "content_type": "Journal Article",
    },
    {
        "title": "Why We Sleep: A Neuroscientist Explains",
        "summary": (
            "Sleep researchers have identified four distinct functions of sleep: metabolic waste clearance, "
            "memory consolidation, immune regulation, and emotional processing. The Conversation's "
            "summary explains why cutting sleep to work more is almost always counterproductive."
        ),
        "url": "https://theconversation.com/why-we-sleep-a-neuroscientist-explains-the-science-of-slumber-161344",
        "author": "The Conversation",
        "tags": "medicine, wellbeing, habits",
        "content_type": "Magazine Article",
    },

    # ── LEARNING & EDUCATION ────────────────────────────────────────────────

    {
        "title": "How to Get Better at the Things You Care About",
        "summary": (
            "Most professionals plateau early because they spend careers in the OK plateau — doing "
            "comfortable tasks on autopilot. Briceno distinguishes the learning zone from the "
            "performance zone and explains why alternating between them drives long-term improvement."
        ),
        "url": "https://www.ted.com/talks/eduardo_briceno_how_to_get_better_at_the_things_you_care_about",
        "author": "Eduardo Briceno",
        "tags": "learning, habits, management",
        "content_type": "TED Talk",
    },
    {
        "title": "The First 20 Hours: How to Learn Anything Fast",
        "summary": (
            "The biggest obstacle to learning is not time but the emotional discomfort of feeling "
            "incompetent in the early hours. Kaufman shows that rapid learning follows a predictable "
            "four-step method and that competence arrives much earlier than most people assume."
        ),
        "url": "https://www.ted.com/talks/josh_kaufman_the_first_20_hours_how_to_learn_anything",
        "author": "Josh Kaufman",
        "tags": "learning, habits, productivity",
        "content_type": "TED Talk",
    },
    {
        "title": "The Power of Spaced Repetition",
        "summary": (
            "The forgetting curve has a powerful antidote: reviewing material at increasing intervals. "
            "Clear explains the science and shows how to apply spaced repetition to medical studies, "
            "language learning, and any knowledge-intensive field."
        ),
        "url": "https://jamesclear.com/spaced-repetition",
        "author": "James Clear",
        "tags": "learning, habits, medicine",
        "content_type": "Blog Post",
    },
    {
        "title": "The Learning Scientists: Retrieval Practice",
        "summary": (
            "Testing yourself on material is one of the most potent learning strategies identified by "
            "cognitive science, yet it is among the least used. This free guide covers the evidence "
            "and practical protocols for study and professional development."
        ),
        "url": "https://www.learningscientists.org/retrieval-practice",
        "author": "The Learning Scientists",
        "tags": "learning, habits, medicine",
        "content_type": "Blog Post",
    },
    {
        "title": "Let's Use Video to Reinvent Education",
        "summary": (
            "Sal Khan accidentally started a global education revolution by posting YouTube math tutorials. "
            "His TED talk explains the pedagogical logic behind Khan Academy — mastery-based progression, "
            "immediate feedback — and what it implies for every professional learning environment."
        ),
        "url": "https://www.ted.com/talks/sal_khan_let_s_use_video_to_reinvent_education",
        "author": "Sal Khan",
        "tags": "learning, education, technology",
        "content_type": "TED Talk",
    },

    # ── CREATIVITY & INNOVATION ─────────────────────────────────────────────

    {
        "title": "Your Elusive Creative Genius",
        "summary": (
            "Elizabeth Gilbert argues the tormented artist mythology is psychologically damaging. "
            "The ancient model of an external muse provides surprising psychological protection "
            "for creative professionals facing fear and self-doubt."
        ),
        "url": "https://www.ted.com/talks/elizabeth_gilbert_your_elusive_creative_genius",
        "author": "Elizabeth Gilbert",
        "tags": "creativity, psychology, wellbeing",
        "content_type": "TED Talk",
    },
    {
        "title": "Where Good Ideas Come From",
        "summary": (
            "Steven Johnson traces the intellectual environments that produce the most innovations — "
            "from coffee houses to coral reefs — and finds a common pattern: liquid networks where "
            "ideas collide and recombine across disciplinary borders."
        ),
        "url": "https://www.ted.com/talks/steven_johnson_where_good_ideas_come_from",
        "author": "Steven Johnson",
        "tags": "creativity, innovation, learning",
        "content_type": "TED Talk",
    },
    {
        "title": "Want to Be More Creative? Go for a Walk",
        "summary": (
            "A Stanford study found that walking boosted creative output by an average of 81% — "
            "and the effect persisted after sitting back down. Oppezzo explains the neuroscience of "
            "divergent thinking and why your best ideas often come away from a desk."
        ),
        "url": "https://www.ted.com/talks/marily_oppezzo_want_to_be_more_creative_go_for_a_walk",
        "author": "Marily Oppezzo",
        "tags": "creativity, wellbeing, habits",
        "content_type": "TED Talk",
    },
    {
        "title": "How to Build a Company Where the Best Ideas Win",
        "summary": (
            "Ray Dalio built Bridgewater on radical transparency and algorithmic decision-making "
            "that counterbalances cognitive bias and political influence. His TED talk applies directly "
            "to any institution where status or seniority can override better evidence."
        ),
        "url": "https://www.ted.com/talks/ray_dalio_how_to_build_a_company_where_the_best_ideas_win",
        "author": "Ray Dalio",
        "tags": "creativity, leadership, decision-making",
        "content_type": "TED Talk",
    },

    # ── COMMUNICATION & NEGOTIATION ─────────────────────────────────────────

    {
        "title": "Harnessing the Science of Persuasion",
        "summary": (
            "Six universal principles govern why people say yes: reciprocity, commitment, social proof, "
            "authority, liking, and scarcity. Cialdini's framework is as useful for building trust "
            "ethically as it is for recognizing when you are being influenced."
        ),
        "url": "https://hbr.org/2001/10/harnessing-the-science-of-persuasion",
        "author": "Robert Cialdini",
        "tags": "negotiation, psychology, behaviour",
        "content_type": "Magazine Article",
    },
    {
        "title": "The Secret Structure of Great Talks",
        "summary": (
            "Nancy Duarte analyzed every great speech and found a shared structure: moving between "
            "what is and what could be, creating tension that only resolves when the audience acts. "
            "The best single resource for communicating complex ideas to any audience."
        ),
        "url": "https://www.ted.com/talks/nancy_duarte_the_secret_structure_of_great_talks",
        "author": "Nancy Duarte",
        "tags": "communication, leadership, creativity",
        "content_type": "TED Talk",
    },
    {
        "title": "How to Speak So That People Want to Listen",
        "summary": (
            "Julian Treasure identifies the seven deadly sins of speaking and explains the four "
            "foundations of powerful speech: Honesty, Authenticity, Integrity, Love. Simple, "
            "memorable, and immediately applicable in clinical and professional settings."
        ),
        "url": "https://www.ted.com/talks/julian_treasure_how_to_speak_so_that_people_want_to_listen",
        "author": "Julian Treasure",
        "tags": "communication, leadership, medicine",
        "content_type": "TED Talk",
    },
    {
        "title": "10 Ways to Have a Better Conversation",
        "summary": (
            "Most people are not listening — they are waiting to talk. Former NPR host Celeste Headlee "
            "identifies ten habits that make every conversation better, starting with the hardest: "
            "actually listening rather than multitasking."
        ),
        "url": "https://www.ted.com/talks/celeste_headlee_10_ways_to_have_a_better_conversation",
        "author": "Celeste Headlee",
        "tags": "communication, medicine, psychology",
        "content_type": "TED Talk",
    },
    {
        "title": "The Danger of a Single Story",
        "summary": (
            "Single stories — incomplete narratives that flatten complexity into stereotype — are not "
            "just politically dangerous but epistemically dangerous. Adichie's TED talk applies equally "
            "to how clinicians form assumptions about patient populations."
        ),
        "url": "https://www.ted.com/talks/chimamanda_ngozi_adichie_the_danger_of_a_single_story",
        "author": "Chimamanda Ngozi Adichie",
        "tags": "psychology, communication, leadership",
        "content_type": "TED Talk",
    },

    # ── TECHNOLOGY & DIGITAL HEALTH ─────────────────────────────────────────

    {
        "title": "The Wonderful and Terrifying Implications of Computers That Can Learn",
        "summary": (
            "Jeremy Howard shows in real time how a laptop running modern deep learning identifies "
            "diseases in medical images at radiologist-level accuracy. One of the clearest introductions "
            "to machine learning for a clinical audience — before AI doctor became marketing copy."
        ),
        "url": "https://www.ted.com/talks/jeremy_howard_the_wonderful_and_terrifying_implications_of_computers_that_can_learn",
        "author": "Jeremy Howard",
        "tags": "technology, medicine, learning",
        "content_type": "TED Talk",
    },
    {
        "title": "Your Data Is Being Weaponized Against You",
        "summary": (
            "Zeynep Tufekci explains how social media data is used not just to target voters but "
            "to suppress opposition. The psychological profiling methods she describes are increasingly "
            "used in healthcare marketing, insurance underwriting, and employer screening."
        ),
        "url": "https://www.ted.com/talks/zeynep_tufekci_we_re_building_a_dystopia_just_to_make_people_click_on_ads",
        "author": "Zeynep Tufekci",
        "tags": "technology, psychology, systems",
        "content_type": "TED Talk",
    },

    # ── FINANCE & ECONOMICS ─────────────────────────────────────────────────

    {
        "title": "The Psychology of Money",
        "summary": (
            "Doing well with money has little to do with intelligence and everything to do with behavior: "
            "patience, humility, and the ability to avoid catastrophic errors. The highest form of wealth "
            "is the ability to wake up and say — I can do whatever I want today."
        ),
        "url": "https://collabfund.com/blog/the-psychology-of-money/",
        "author": "Morgan Housel",
        "tags": "finance, psychology, personal development",
        "content_type": "Essay",
    },
    {
        "title": "The Seduction of Pessimism",
        "summary": (
            "Pessimism sounds sophisticated; optimism sounds naive. But the historical record "
            "overwhelmingly favors long-term optimism. Housel argues that pessimistic narratives "
            "have a structural advantage in media that systematically distorts our long-term decisions."
        ),
        "url": "https://collabfund.com/blog/the-seduction-of-pessimism/",
        "author": "Morgan Housel",
        "tags": "finance, psychology, strategy",
        "content_type": "Essay",
    },
    {
        "title": "What Are You Optimizing For?",
        "summary": (
            "Most people never make their implicit optimization function explicit — and as a result, "
            "optimize for status and short-term income at the expense of autonomy, meaningful "
            "relationships, and health. A short but clarifying essay on career and life design."
        ),
        "url": "https://collabfund.com/blog/what-are-you-optimizing-for/",
        "author": "Morgan Housel",
        "tags": "personal development, strategy, finance",
        "content_type": "Essay",
    },
    {
        "title": "Why Doctors Should Care About Financial Planning",
        "summary": (
            "Physicians have among the highest professional incomes yet also among the highest rates "
            "of financial stress and late retirement. White Coat Investor's free primer covers the "
            "five most common financial mistakes physicians make and provides a practical starting framework."
        ),
        "url": "https://www.whitecoatinvestor.com/financial-planning-for-doctors/",
        "author": "The White Coat Investor",
        "tags": "finance, medicine, personal development",
        "content_type": "Blog Post",
    },
    {
        "title": "How Economic Inequality Harms Societies",
        "summary": (
            "Richard Wilkinson presents data from 23 developed countries showing that inequality — "
            "not average income — predicts mental illness, imprisonment, teenage pregnancy, life "
            "expectancy, and social mobility. One of the most cited talks on social determinants of health."
        ),
        "url": "https://www.ted.com/talks/richard_wilkinson_how_economic_inequality_harms_societies",
        "author": "Richard Wilkinson",
        "tags": "finance, medicine, systems",
        "content_type": "TED Talk",
    },

    # ── SYSTEMS THINKING ────────────────────────────────────────────────────

    {
        "title": "Systems Thinking: The Essential Introduction",
        "summary": (
            "Farnam Street's guide explains feedback loops, stocks and flows, and delays — the three "
            "structural elements that determine how systems behave over time. Essential for anyone "
            "managing complex adaptive systems, from ICUs to health policy."
        ),
        "url": "https://fs.blog/systems-thinking/",
        "author": "Shane Parrish",
        "tags": "systems, decision-making, strategy",
        "content_type": "Blog Post",
    },
    {
        "title": "Survivorship Bias: The Invisible Graveyard",
        "summary": (
            "We see the companies that succeeded and systematically miss the far larger pool of "
            "failures that never made it into the data. Farnam Street explains how this corrupts "
            "medical research, business strategy, and self-help advice."
        ),
        "url": "https://fs.blog/survivorship-bias/",
        "author": "Shane Parrish",
        "tags": "decision-making, medicine, systems",
        "content_type": "Blog Post",
    },
    {
        "title": "The Map Is Not the Territory",
        "summary": (
            "Models are simplifications of reality. The danger is forgetting that — and treating "
            "the map as if it were the territory. This mental model applies to clinical guidelines, "
            "economic forecasts, and any organization that confuses its strategy document with reality."
        ),
        "url": "https://fs.blog/map-and-territory/",
        "author": "Shane Parrish",
        "tags": "decision-making, systems, medicine",
        "content_type": "Blog Post",
    },
    {
        "title": "Why Every System Eventually Breaks Down",
        "summary": (
            "Nassim Taleb's concept of antifragility — systems that gain from disorder — offers a "
            "counterintuitive design principle: the goal is not robustness but the ability to benefit "
            "from stressors. Farnam Street unpacks the concept with healthcare implications."
        ),
        "url": "https://fs.blog/antifragile/",
        "author": "Shane Parrish",
        "tags": "systems, strategy, decision-making",
        "content_type": "Blog Post",
    },
    {
        "title": "Circle of Competence",
        "summary": (
            "Knowing exactly where the boundary of your competence lies — and never crossing it without "
            "realizing it — is the mental model behind Buffett and Munger's investment discipline. "
            "Intellectual humility is a high-performance strategy, not just a virtue."
        ),
        "url": "https://fs.blog/circle-of-competence/",
        "author": "Shane Parrish",
        "tags": "decision-making, strategy, psychology",
        "content_type": "Blog Post",
    },
    {
        "title": "Occam's Razor: How to Cut Through the Noise",
        "summary": (
            "When two explanations fit the same data, prefer the simpler one. One of the most useful "
            "heuristics in medicine, science, and decision-making — and one of the most frequently "
            "violated. Farnam Street explains when simplicity is a virtue and when it becomes a liability."
        ),
        "url": "https://fs.blog/occams-razor/",
        "author": "Shane Parrish",
        "tags": "decision-making, medicine, systems",
        "content_type": "Blog Post",
    },

    # ── PERSONAL DEVELOPMENT ────────────────────────────────────────────────

    {
        "title": "Grit: The Power of Passion and Perseverance",
        "summary": (
            "Duckworth left a consulting job to teach math, then spent a decade studying why talent "
            "alone does not predict achievement. Her answer — grit, the combination of passion and "
            "perseverance — is one of the most replicable predictors of long-term success."
        ),
        "url": "https://www.ted.com/talks/angela_lee_duckworth_grit_the_power_of_passion_and_perseverance",
        "author": "Angela Duckworth",
        "tags": "psychology, habits, personal development",
        "content_type": "TED Talk",
    },
    {
        "title": "How to Be Successful",
        "summary": (
            "Sam Altman's extended essay on compound growth applied to people: working on problems "
            "that matter, building leverage through knowledge and network, and developing the "
            "confidence to persist without external validation."
        ),
        "url": "https://blog.samaltman.com/how-to-be-successful",
        "author": "Sam Altman",
        "tags": "personal development, strategy, leadership",
        "content_type": "Blog Post",
    },
    {
        "title": "The Days Are Long but the Decades Are Short",
        "summary": (
            "Written on his 30th birthday, Sam Altman's short essay is a distillation of what he'd "
            "learned about time, money, relationships, and work. Ruthlessly direct about the trade-offs "
            "that define a life, and honest about what most high-achievers discover too late."
        ),
        "url": "https://blog.samaltman.com/the-days-are-long-but-the-decades-are-short",
        "author": "Sam Altman",
        "tags": "personal development, strategy, wellbeing",
        "content_type": "Blog Post",
    },
    {
        "title": "The Anatomy of Determination",
        "summary": (
            "Determination is the most important factor in professional achievement. Graham breaks it "
            "into two components: resilience (the ability to bounce back from setbacks) and relentlessness "
            "(continuous forward motion). He argues determination can be cultivated through deliberate framing."
        ),
        "url": "https://paulgraham.com/determination.html",
        "author": "Paul Graham",
        "tags": "psychology, personal development, habits",
        "content_type": "Essay",
    },
    {
        "title": "What You Can't Say",
        "summary": (
            "Every era has ideas that cannot be expressed openly. Graham's exercise in intellectual "
            "courage: what would people look back on in 2050, scandalized by what we currently take "
            "for granted? The essay trains the reader to think outside the window of acceptable opinion."
        ),
        "url": "https://paulgraham.com/say.html",
        "author": "Paul Graham",
        "tags": "psychology, creativity, personal development",
        "content_type": "Essay",
    },
    {
        "title": "Ikigai: The Japanese Concept That Will Help You Find Your Purpose",
        "summary": (
            "Ikigai — reason for being — is the intersection of what you love, what you are good at, "
            "what the world needs, and what you can be paid for. It is associated with Okinawan culture "
            "and some of the world's highest life expectancy and lowest rates of dementia."
        ),
        "url": "https://ikigaitribe.com/ikigai/the-japanese-concept-of-ikigai/",
        "author": "Ikigai Tribe",
        "tags": "personal development, wellbeing, strategy",
        "content_type": "Blog Post",
    },
    {
        "title": "Before the Startup",
        "summary": (
            "Most startup advice optimizes for the wrong things. Graham: get good at something, work "
            "with people you like, and solve problems you have actually experienced. Applies broadly "
            "to anyone building something new inside or outside a formal institution."
        ),
        "url": "https://paulgraham.com/before.html",
        "author": "Paul Graham",
        "tags": "entrepreneurship, strategy, personal development",
        "content_type": "Essay",
    },
    {
        "title": "The Refragmentation",
        "summary": (
            "The post-war era of mass conformity was a historical anomaly that is now ending. Graham "
            "argues that fragmentation of culture and career paths creates more individual opportunity "
            "but also more uncertainty — useful context for understanding why career planning has gotten harder."
        ),
        "url": "https://paulgraham.com/re.html",
        "author": "Paul Graham",
        "tags": "strategy, personal development, systems",
        "content_type": "Essay",
    },
    {
        "title": "Why We Have Too Few Women Leaders",
        "summary": (
            "Sheryl Sandberg's pre-Lean In TED talk argues that internal barriers hold women back from "
            "leadership positions as much as structural ones. Medicine has some of the starkest gender "
            "gaps in senior leadership of any profession."
        ),
        "url": "https://www.ted.com/talks/sheryl_sandberg_why_we_have_too_few_women_leaders",
        "author": "Sheryl Sandberg",
        "tags": "leadership, management, psychology",
        "content_type": "TED Talk",
    },
    {
        "title": "3 Ways to Be a Better Ally in the Workplace",
        "summary": (
            "Being a passive bystander in moments of workplace inequity is itself a form of participation. "
            "Epler covers three specific behaviors — seeing people, amplifying voices, and speaking up — "
            "that any professional can implement immediately regardless of their position."
        ),
        "url": "https://www.ted.com/talks/melinda_briana_epler_3_ways_to_be_a_better_ally_in_the_workplace",
        "author": "Melinda Epler",
        "tags": "leadership, management, communication",
        "content_type": "TED Talk",
    },

    # ── PHYSICIAN MBA & STRATEGY ────────────────────────────────────────────

    {
        "title": "The Explainer: Disruptive Innovation",
        "summary": (
            "Clayton Christensen's theory of disruptive innovation is also widely misapplied. "
            "This free Christensen Institute explainer clarifies what the theory actually says and "
            "why understanding the distinction matters for anyone trying to change a complex institution."
        ),
        "url": "https://www.christenseninstitute.org/disruptive-innovations/",
        "author": "Clayton Christensen Institute",
        "tags": "strategy, management, technology",
        "content_type": "Essay",
    },
    {
        "title": "What Is Strategy?",
        "summary": (
            "Porter distinguishes operational effectiveness — doing the same things better — from strategy: "
            "doing different things. Trade-offs, not best practices, are the source of sustainable "
            "competitive advantage. Foundational for any physician entering healthcare leadership."
        ),
        "url": "https://www.youtube.com/watch?v=mYF2_FBCvXw",
        "author": "Michael Porter",
        "tags": "strategy, management, leadership",
        "content_type": "Video Talk",
    },
    {
        "title": "The Lean Startup Method",
        "summary": (
            "Build-measure-learn feedback loops and minimum viable products have been adopted by hospital "
            "innovation labs, public health programs, and global development organizations. "
            "This free summary covers the core principles of Ries's foundational framework."
        ),
        "url": "https://theleanstartup.com/principles",
        "author": "Eric Ries",
        "tags": "strategy, entrepreneurship, systems",
        "content_type": "Essay",
    },
    {
        "title": "The Strategic Use of Stories in Medicine",
        "summary": (
            "Narrative medicine — listening to and interpreting patients' illness stories — improves "
            "diagnostic accuracy, patient adherence, and clinical satisfaction. Rita Charon's Columbia "
            "lecture explains the theory and practical application in clinical training and practice."
        ),
        "url": "https://www.youtube.com/watch?v=24kHX2HtU3o",
        "author": "Rita Charon",
        "tags": "medicine, communication, leadership",
        "content_type": "Video Talk",
    },
    {
        "title": "The Honest Truth About Dishonesty",
        "summary": (
            "Ariely's research shows most dishonesty is not calculated but opportunistic — people cheat "
            "just a little and maintain their self-image as honest. His TED talk has direct implications "
            "for medical billing, research integrity, and team accountability."
        ),
        "url": "https://www.ted.com/talks/dan_ariely_our_buggy_moral_code",
        "author": "Dan Ariely",
        "tags": "behaviour, decision-making, management",
        "content_type": "TED Talk",
    },
    {
        "title": "The Hidden Influence of Social Networks",
        "summary": (
            "Behaviors — smoking, obesity, happiness, loneliness — spread through social networks like "
            "contagion, up to three degrees of separation. Christakis and Fowler's research has radical "
            "implications for public health interventions."
        ),
        "url": "https://www.ted.com/talks/nicholas_christakis_the_hidden_influence_of_social_networks",
        "author": "Nicholas Christakis",
        "tags": "medicine, behaviour, systems",
        "content_type": "TED Talk",
    },
    {
        "title": "The Surprising Science of Happiness",
        "summary": (
            "Dan Gilbert's research on synthetic happiness reveals that humans are systematically wrong "
            "about what will make them happy. His experiments on the psychological immune system have "
            "profound implications for medical decision-making and informed consent."
        ),
        "url": "https://www.ted.com/talks/dan_gilbert_the_surprising_science_of_happiness",
        "author": "Dan Gilbert",
        "tags": "psychology, wellbeing, decision-making",
        "content_type": "TED Talk",
    },
    {
        "title": "How to Know What You Don't Know",
        "summary": (
            "Curiosity is driven by a gap between what we know and what we want to know. Celeste Kidd "
            "explains what happens when institutional environments suppress the questioning mind — "
            "and what conditions preserve the inquisitiveness that drives both science and good medicine."
        ),
        "url": "https://www.ted.com/talks/celeste_kidd_how_to_know_what_you_don_t_know",
        "author": "Celeste Kidd",
        "tags": "learning, psychology, creativity",
        "content_type": "TED Talk",
    },

]


def seed_articles(db):
    """Insert seed articles if the articles table is empty.
    Also back-fills content_type for any pre-existing articles that still have
    the old default value of 'Article' and whose URL matches a known seed.
    Inserts any new seed articles that do not yet exist (by URL).

    Seeds use added_by=None, marking them as global suggestions available to all
    users via the home-page recommendation engine. They are NOT shown in any
    user's Browse Library — users build that themselves.
    """
    from models.article import Article

    if Article.query.count() == 0:
        for data in SEED_ARTICLES:
            db.session.add(Article(added_by=None, **data))
        db.session.commit()
        print(f"Seeded {len(SEED_ARTICLES)} articles.")
        return

    # Back-fill content_type for existing seed records with old default
    url_to_type = {a["url"]: a["content_type"] for a in SEED_ARTICLES}
    updated = 0
    for article in Article.query.filter(
        Article.added_by.is_(None),
    ).all():
        if article.url in url_to_type and article.content_type != url_to_type[article.url]:
            article.content_type = url_to_type[article.url]
            updated += 1
    if updated:
        db.session.commit()
        print(f"Back-filled content_type on {updated} articles.")

    # Insert any new seed articles that do not yet exist (by URL)
    existing_urls = {a.url for a in Article.query.filter(Article.added_by.is_(None)).all()}
    new_articles = [a for a in SEED_ARTICLES if a["url"] not in existing_urls]
    if new_articles:
        for data in new_articles:
            db.session.add(Article(added_by=None, **data))
        db.session.commit()
        print(f"Added {len(new_articles)} new seed articles.")
