from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

questions = [
    {
        'question': 'ما هو تعريف الاحتباس الحراري؟',
        'choices': ['ارتفاع درجة حرارة الأرض', 'ذوبان الجليد فقط', 'زيادة الغازات السامة'],
        'answers': [0, 2],
    },
    {
        'question': 'ما هي الغازات المسببة له؟',
        'choices': ['ثاني أكسيد الكربون', 'الميثان', 'الأوكسجين'],
        'answers': [0, 1],
    },
    {
        'question': 'ما هو تأثير قطع الأشجار؟',
        'choices': ['يقلل الأكسجين', 'يزيد ثاني أكسيد الكربون', 'يحسن المناخ'],
        'answers': [0, 1],
    },
    {
        'question': 'ما آثار الاحتباس الحراري؟',
        'choices': ['ذوبان الجليد', 'ارتفاع منسوب البحار', 'انخفاض درجات الحرارة'],
        'answers': [0, 1],
    },
    {
        'question': 'ما هو الحل الأفضل للتقليل من الاحتباس الحراري؟',
        'choices': ['زرع الأشجار', 'الاعتماد على الطاقة المتجددة', 'زيادة المصانع'],
        'answers': [0, 1],
    },
    {
        'question': 'أين يحدث الاحتباس الحراري؟',
        'choices': ['في المدن فقط', 'على كوكب الأرض', 'في القطب الشمالي فقط'],
        'answers': [1],
    },
    {
        'question': 'كيف يمكن للأفراد المساعدة؟',
        'choices': ['إطفاء الأنوار غير الضرورية', 'استخدام السيارات أكثر', 'إعادة التدوير'],
        'answers': [0, 2],
    },
    {
        'question': 'أي مما يلي يسبب الاحتباس الحراري؟',
        'choices': ['الوقود الأحفوري', 'الماء', 'الهواء'],
        'answers': [0],
    },
    {
        'question': 'كيف تؤثر المصانع على البيئة؟',
        'choices': ['تزيد من الغازات الضارة', 'تقلل الأوكسجين', 'تحسن التربة'],
        'answers': [0, 1],
    },
    {
        'question': 'هل هناك علاقة بين الاحتباس الحراري والتلوث؟',
        'choices': ['نعم', 'لا'],
        'answers': [0],
    },
    {
        'question': 'أي نشاط يزيد من انبعاث الغازات؟',
        'choices': ['حرق النفايات', 'التدوير', 'المشي'],
        'answers': [0],
    },
    {
        'question': 'ما هي فوائد الطاقة المتجددة؟',
        'choices': ['تقلل الانبعاثات', 'لا تضر البيئة', 'تزيد الاحتباس الحراري'],
        'answers': [0, 1],
    },
    {
        'question': 'لماذا نزرع الأشجار؟',
        'choices': ['تمتص ثاني أكسيد الكربون', 'تزيد من التلوث', 'تحمي الغلاف الجوي'],
        'answers': [0, 2],
    },
    {
        'question': 'ما هو أثر ذوبان الجليد؟',
        'choices': ['ارتفاع مستوى البحار', 'انخفاض درجة الحرارة', 'اختفاء بعض الجزر'],
        'answers': [0, 2],
    },
    {
        'question': 'كيف نُقلل من استهلاك الطاقة؟',
        'choices': ['استخدام المصابيح الموفرة', 'تشغيل الأجهزة دون داعي', 'الاعتماد على الشمس'],
        'answers': [0, 2],
    }
]

def load_scores():
    if os.path.exists("scores.json"):
        with open("scores.json", "r") as f:
            return json.load(f)
    return {}

def save_scores(scores):
    with open("scores.json", "w") as f:
        json.dump(scores, f)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        return redirect(url_for("exam"))
    return render_template("index.html")

@app.route("/exam", methods=["GET", "POST"])
def exam():
    if request.method == "POST":
        name = request.form["name"]
        score = 0
        correct_count = 0  # عدد الإجابات الصحيحة

        total_correct_answers = 0  # عدد الإجابات الصحيحة للمقارنة
        total_selected_answers = 0  # عدد الإجابات التي تم اختيارها من قبل الطالب

        for i, question in enumerate(questions):
            selected = request.form.getlist(f"question{i}")  # الإجابات المختارة
            selected = list(map(int, selected))  # تحويل الإجابات المختارة إلى أرقام

            correct_answers = question["answers"]  # الإجابات الصحيحة لهذا السؤال

            # حساب الإجابات الصحيحة التي تم اختيارها
            true_positives = len(set(selected) & set(correct_answers))  # الإجابات الصحيحة التي تم اختيارها
            false_positives = len(set(selected) - set(correct_answers))  # الإجابات الخاطئة التي تم اختيارها

            correct_count += true_positives  # زيادة عدد الإجابات الصحيحة

            # حساب النقاط
            if len(correct_answers) > 0:
                total_correct_answers += len(correct_answers)  # عدد الإجابات الصحيحة المتوقعة
                total_selected_answers += len(selected)  # عدد الإجابات التي اختارها الطالب

        # حساب النقاط بناءً على إجابات صحيحة وأجوبة خاطئة
        if total_correct_answers > 0:
            raw_score = (correct_count / total_correct_answers) * 20
            score = round(raw_score, 2)

        # حفظ النتائج
        scores = load_scores()
        scores[name] = score
        save_scores(scores)

        # إعادة عرض النتيجة
        return render_template("result.html", name=name, score=score, correct=correct_count, total=len(questions))

    return render_template("examen.html", questions=questions)


@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if request.method == "POST":
        password = request.form["password"]
        if password == "GnO6XKz$Bl":
            scores = load_scores()
            return render_template("dashboard.html", scores=scores)
        else:
            return "كلمة المرور خاطئة!"
    return render_template("password.html")

if __name__ == "__main__":
    app.run(debug=True)
