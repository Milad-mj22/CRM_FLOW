import json
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from TasksManager.models import CommentTask, Task
# Create your views here.
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt




@login_required
def user_tasks_json(request):
    tasks = Task.objects.filter(assigned_to=request.user)
    data = []

    
    for task in tasks:
        comments_qs = CommentTask.objects.filter(task_id=task.id)
        comment_list = [
            {
                'id': comment.id,
                'description': comment.description,
                'created_date': comment.created_date.strftime('%Y-%m-%d'),
                'created_by':  comment.created_by.username
            }
            for comment in comments_qs
        ]

        data.append({
            'id': task.id,
            'title': task.title,
            'is_done' : task.is_done,
            'created_by' : task.created_by.username,
            'buyer': {
                'id': task.buyer.id if task.buyer else None,
                'username': task.buyer.first_name if task.buyer else None
            },
            'start': task.due_date.strftime('%Y-%m-%d'),
            'color':  "#058f1c" if task.is_done  else '#e67e22',
            'allDay': True,
            'comments': comment_list
        })

    undone_data = []
    for task in tasks:
        undone_data.append({
            'id': task.id,
            'title': task.title,
            'due_date': task.due_date.strftime('%Y-%m-%d'),
            'buyer': {
                'id': task.buyer.id,
                'username': task.buyer.first_name
            } if task.buyer else None,
        })
    # data['undone_data'] = undone_data
    # data = [data,undone_data]

    return JsonResponse(data=data, safe=False)

@login_required
def calendar_view(request):
    return render(request, 'tasks/dashboard_calendar.html')









@csrf_exempt
def update_task(request, task_id):
    if request.method == 'POST':
        task = Task.objects.get(id=task_id, assigned_to=request.user)
        data = json.loads(request.body)

        task.is_done = data.get('done', False)
        task.save()

        comment = data.get('comment', '')
        if comment !='':
            CommentTask.objects.create(task_id=task,description=comment,created_by=request.user)
     

        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)





def create_task(created_by,title,description,due_date,assigned_to,buyer=None):

    Task.objects.create(
        title=title,
        description=description,
        due_date=due_date,
        assigned_to=assigned_to,
        created_by=created_by,
        buyer = buyer
    )



