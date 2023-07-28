

from django.shortcuts import render ,get_object_or_404,redirect
# Create your views here.
from book.models import Book,Category,Order,Feedback

from user.models import Address
from django.conf import settings
from django.core.mail import send_mail


from django.template.loader import render_to_string
from django.utils.html import strip_tags
from datetime import time,date,timedelta




def all_books(request):
    books=Book.objects.all()
    categories=Category.objects.all().order_by('category')
    #print(books.query)
    context={
        "books":books,
        "categories":categories
    }
    return render(request,"book/books.html",context)

def book_details(request,id):
    #book=Book.objects.get(id=id)
    book=get_object_or_404(Book,id=id)
    quantity=1
    if request.session.get("cart_items"):
        if request.session.get('cart_items').get(str(id)):
            quantity=request.session.get("cart_items")[str(id)]
    context={
        'book':book,
        'quantity':quantity
    }
    return render(request,"book/book_details.html",context)

def book_category(request,cid):
    books=Book.objects.filter(category=cid)
    categories=Category.objects.all().order_by('category')
    # print(books.query)
    context={
        "books":books,
        "categories":categories
    }
    return render(request,"book/books.html",context)


def add_to_cart(request):
    if request.method=="POST":
        book_id=request.POST.get("book_id")
        quantity=request.POST.get("quantity")
        cart_items={}
        if request.session.get("cart_items"):
            cart_items=request.session.get("cart_items")
        cart_items[book_id]=quantity
        request.session["cart_items"]=cart_items
        print(request.session.get("cart_items"))
    return redirect("all_books")


def cart(request):
    cart_details,total_price =get_cart_details(request)
    context={
        "books":cart_details,
        "total_price":total_price
    }
    return render(request,"book/cart.html",context)

def get_cart_details(request):
    cart_items=request.session.get('cart_items')
    books=Book.objects.filter(id__in=list(cart_items.keys()))
    total_price=0
    cart_details=[]
    for book in books:
        quantity=int(cart_items[str(book.id)])
        price=quantity*book.price
        total_price+=price
        cart_details.append({
            "id":book.id,
            "title":book.title,
            "quantity":quantity,
            "price":price,
            "image":book.image
                
        })
    return cart_details,total_price


def remove_from_cart(request,id):
    cart_items=request.session.get('cart_items')
    del cart_items[str(id)]
    request.session['cart_items']=cart_items
    return redirect('cart') 


def check_out(request):
    addresses=Address.objects.filter(user=request.user)
    cart_details,total_price=get_cart_details(request)
    context={
        "addresses":addresses,
        "books":cart_details,
        'total_price':total_price
    } 
    return render(request,'book/check_out.html',context)


def place_order(request):
    if request.method=="POST":
        user=request.user
        address=request.POST.get("address")
        address=Address.objects.get(id=address)
        payment_mode=request.POST.get('payment_mode')
        cart_details,total_price=get_cart_details(request)
        orders=[]
        for book in cart_details:
            order = Order(
                book = Book.objects.get(id=book['id']),
                user = user,
                address = address,
                quantity = book['quantity'],
                price = book['price'],
                payment_method = payment_mode
            )
            orders.append(order)
    Order.objects.bulk_create(orders)
    
    subject="Order placed sucesssfully"
    mail_context={
        "username":request.user.first_name+" "+request.user.last_name,
        "books": cart_details,
        "addresss":address,
        "delivery_date": date.today() + timedelta(days=7),
        "total_price":total_price
    }
    html_message=render_to_string('book/mail_template.html',mail_context)
    plain_message=strip_tags(html_message)
    #body=f"Your Order is placed sucessfully. Amount {total_price}.Delivery address:{address}"
    to=[request.user.email,]
    from_email=settings.EMAIL_HOST_USER
    #send_mail(subject=subject,message=body,from_email=from_email,recipient_list=to,fail_silently=False)
    send_mail(subject=subject,message=plain_message,from_email=from_email,recipient_list=to,fail_silently=False)
    request.session['cart_items']={} 
    return redirect('all_books')


def orders(request):
    orders=Order.objects.filter(user=request.user).order_by('id')
    context={
        'orders':orders
    }
    return render(request,'book/orders.html',context)



def add_feedback(request):
    if request.method=="POST":
        user=request.user
        book_id=request.POST.get("book_id")
        book=Book.objects.get(id=book_id)
        rating=request.POST.get("rating")
        comment=request.POST.get("comment")
        feedback=None
        try:
            feedback=Feedback.objects.get(user=user,book=book)
        except:
            print("comment is not available")
        if feedback is None:
            feedback=Feedback
            feedback.user=user
            feedback.book=book
        feedback.rating=rating
        feedback.comment=comment
        feedback.save()
        return redirect("all_books")
            