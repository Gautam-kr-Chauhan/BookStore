from django.shortcuts import render,HttpResponse

#from django.contrib 
# Create your views here.
def index(request):
    #return HttpResponse("<h1> Hello World</h1>")
    return render(request,'pages/index.html')

def about(request):
    #name="john"
    student={1:"john",2:"smith",3:"kriti",4:"kapoor"}
    result={
        1:{"name":"john","cgpa":[9.2,9.8,9.1,9.7]},
        2:{"name":"smith","cgpa":[9.2,9.8,9.1,9.7]},
        3:{"name":"riya","cgpa":[9.2,9.8,9.1,9.7]},
        4:{"name":"kriti","cgpa":[9.2,9.8,9.1,9.7]},
        5:{"name":"mandhana","cgpa":[9.2,9.8,9.1,9.7]},
        
    }
    context={
        "name":"sam",
        "age":23,
        "num1":12,
        "num2":4,
        "nums":[1,2,3,4,5],
        'students':student,
        'results':result
    }
    return render(request, 'pages/about.html',context)