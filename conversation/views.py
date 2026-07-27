from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from items.models import Item
from .models import Conversation
from .forms import ConversationMessageForm

@login_required
def inbox(request):
    conversations = Conversation.objects.filter(members__in=[request.user.id])
    
    return render(request, 'conversation/inbox.html', {
        'conversations': conversations
    })

@login_required
def detail(request, pk):
    conversation = Conversation.objects.filter(members__in=[request.user.id]).get(pk=pk)

    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)

        if form.is_valid():
            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()

            conversation.save()

            return redirect('conversation:detail', pk=pk)
    else:
        form = ConversationMessageForm()

    return render(request, 'conversation/detail.html', {
        'conversation': conversation,
        'form': form
    })

@login_required
def new_conversation(request, item_pk):
    item = get_object_or_404(Item, pk=item_pk)

    # ১. ইউজার যদি নিজেই এই আইটেমের মালিক হয়, তবে তাকে চ্যাট করতে দেবে না
    if item.created_by == request.user:
        return redirect('/')

    # ২. এই আইটেম নিয়ে ইউজারের সাথে সেলারের আগের কোনো কনভারসেশন আছে কি না
    existing_conversations = Conversation.objects.filter(item=item).filter(members__in=[request.user.id])

    # ৩. যদি আগে থেকেই চ্যাট থেকে থাকে, তবে নতুন চ্যাট না খুলে সরাসরি পুরনো চ্যাটে পাঠাবে
    if existing_conversations.exists():
        return redirect('conversation:detail', pk=existing_conversations.first().id)

    # ৪. নতুন মেসেজ পাঠানোর হ্যান্ডলিং
    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)

        if form.is_valid():
            conversation = Conversation.objects.create(item=item)
            conversation.members.add(request.user)
            conversation.members.add(item.created_by)
            conversation.save()

            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()

            return redirect('conversation:detail', pk=conversation.id)
    else:
        form = ConversationMessageForm()

    return render(request, 'conversation/new.html', {
        'form': form
    })