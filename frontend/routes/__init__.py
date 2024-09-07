from flask import Flask, render_template

app = Flask(__name__)



@app.get("/home")
def home_page():
    list = ["member_commands","role_commands","topic_commands","lesson_commands","group_commands"]
    return render_template("home.html",commands=list)



@app.get("/member_commands")
def member_commands():
    commands = ["create_member","see_all_members","delete_all_members","see_one_member","delete_one_member","update_member"]
    return render_template("commands.html", commands=commands)

@app.get("/role_commands")
def role_commands():
    commands = ["create_role","see_all_roles","delete_all_roles","see_one_role","delete_one_role","update_role"]
    return render_template("commands.html", commands=commands)

@app.get("/topic_commands")
def topic_commands():
    commands = ["create_topic","see_all_topics","delete_all_topics","see_one_topic","delete_one_topic","update_topic"]
    return render_template("commands.html", commands=commands) 




@app.get("/lesson_commands")
def lesson_commands():
    commands = ["create_lesson","see_all_lessons","delete_all_lessons","see_one_lesson","delete_one_lesson","update_lesson"]
    return render_template("commands.html", commands=commands)


@app.get("/group_commands")
def group_commands():
    commands = ["create_group","see_all_groups","delete_all_groups","see_one_group","delete_one_group","update_group"]
    return render_template("commands.html", commands=commands)


from . import members,roles,lessons,groups,topics


if __name__ == "__main__":
    app.run(debug=True)
