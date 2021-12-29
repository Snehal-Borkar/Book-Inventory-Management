from django.shortcuts import render 
from django.http.response import HttpResponse,HttpResponseRedirect ,JsonResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
import requests
from stores.models import Books, Store 
import json





def showbooks(book_ids,user=None): 
    print(book_ids)
    book_list=[] 
    book_info={} 
    for b in book_ids:
        if isinstance(b, str):
            self_link ="https://www.googleapis.com/books/v1/volumes/"+b 
        else:
            self_link ="https://www.googleapis.com/books/v1/volumes/"+b.book_id
        r=requests.get(self_link)
        data=r.json()
        item =data 
       
        book_id=item["id"]
        book_info["book_id"]=book_id
        if user is not None:
            quantity=Books.objects.get(book_id=book_id,user=user)
            book_info["quantity"]=quantity.number_of_copies  

            if book_info["quantity"]==0:
                book_info["status"]="Out of stock"
            else :
                book_info["status"]="Left"

         

        title= item["volumeInfo"]["title"]
        book_info["title"]=title 

        language= item["volumeInfo"]["language"]
        book_info["language"]=language
        pagecount= item["volumeInfo"]["pageCount"]
        book_info["pagecount"]=pagecount

        if  item["volumeInfo"].get("authors") is not None:
            author= item["volumeInfo"]["authors"]
            book_info["author"]=author  


        if  item["volumeInfo"].get("averageRating") is not None:
            averageRating= item["volumeInfo"]["averageRating"]
            book_info["averageRating"]=averageRating 

        if item["volumeInfo"].get("publisher") is not None:
            publisher= item["volumeInfo"]["publisher"]
            book_info["publisher"]=publisher

        if  item["volumeInfo"].get("publishedDate") is not None:
            publishedDate= item["volumeInfo"]["publishedDate"]
            book_info["publishedDate"]=publishedDate

        if  item["volumeInfo"].get("description") is not None: 
            description= item["volumeInfo"]["description"]
            book_info["description"]=description

        if  item.get("selfLink") is not None:  
            selfLink=item["selfLink"]
            book_info["selfLink"]=selfLink

        
        if  item["volumeInfo"].get("imageLinks") is not None:
            imageLinks= item["volumeInfo"]["imageLinks"]["thumbnail"]
            book_info["imageLinks"]=imageLinks 
            
            
        if  item.get("saleInfo") is not None:

            if item["saleInfo"].get("listPrice") is not None:
                listPrice= item["saleInfo"]["listPrice"]["amount"]
                book_info["listPrice"]=listPrice  

            
            if item["saleInfo"].get("retailPrice") is not None:
                retailPrice= item["saleInfo"]["retailPrice"]["amount"]
                book_info["retailPrice"]=retailPrice  
                 
                currencyCode= item["saleInfo"]["listPrice"]["currencyCode"]
                book_info["currencyCode"]=currencyCode 
        
        book_list.append(book_info.copy())
        book_info.clear()
    return book_list





def stores(request):
    store_q=Store.objects.all()
    return render(request,'stores/all_stores.html',{'stores':store_q,})

def handlelogin(request,id=None):
    if request.method =="POST":
        username=request.POST['username']
        password=request.POST['password']
         
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            user=request.user
            print("request.user:",request.user)
            # return render(request,"stores/Mystore.html",{'username':user})
            return HttpResponseRedirect("/Mystore/")

        else:
            return HttpResponse("<h4> invalid credentials !</h4>") 
    else:
        if id==None:
            return render(request,"stores/login.html")
        else :
            
            mystore=Store.objects.get(id=id)
            return render(request,"stores/login.html",{"mystore":mystore})


def handlelogout(request,):
    logout(request)
    return HttpResponseRedirect("/")


def handleregister(request): 
    if request.method=="POST":
        user=request.user
        Storename=request.POST['storename']
        Username=request.POST['username']
        First_name=request.POST['first_name']
        Last_name=request.POST['last_name']
        Email=request.POST['email']
        Password=request.POST['password']
        Cpassword = request.POST['cpassword']


        users_q=User.objects.all() 
        store_q=Store.objects.all()
        for u in users_q: 
            if Username ==u.username:
                messages.error(request,f"Username {Username} Already exists try another one !")
                return render(request,'stores/all_stores.html',{'stores':store_q, })
        for u in store_q: 
            if Storename ==u.store_name:
                messages.error(request,f"Store Name {Storename} Already exists try another one !")
                return render(request,'stores/all_stores.html',{'stores':store_q, })
 
       
        if len(Username)>10:
            messages.error(request,"Username must be less than 10 characters")
            return render(request,'stores/base.html',{'stores':store_q,})


        if Password!=Cpassword:
            messages.error(request,"Confirmed password not match with passwod you entered ! ")
            return render(request,'stores/all_stores.html',{'stores':store_q,})

        cr_user=User.objects.create_user(Username,Email,Password,is_staff=True)
        cr_user.first_name=First_name
        cr_user.last_name=Last_name
        cr_user.save()
        Store.objects.create(user=cr_user,store_name=Storename) 
        messages.success(request,f"New user {Username} created !")
        # return render(request,'stores/all_stores.html',{'stores':store_q,})
        return HttpResponseRedirect("/")
            
    else:
        
        return HttpResponseRedirect("login/")
 


def addbookpage(request):
    return render(request,"stores/searchedbooks.html")



login_required
def searchedbook(request,book_id=None):
    
    # query=request.GET.get['search']
    query=request.GET.get('search') 
    url="https://www.googleapis.com/books/v1/volumes?q="+query+"&maxResults=40"
    r=requests.get(url)
    data=r.json()
    # data=json.dumps(data)
    list_items=data["items"]
    book_info={}
    short_item_list=[]

    for item in range(len(list_items)): 
        book_id=list_items[item]["id"]
        book_info["book_id"]=book_id

        # title=list_items[item]["volumeInfo"]["title"]
        # book_info["title"]=title

        
        

        language=list_items[item]["volumeInfo"]["language"]
        book_info["language"]=language
        

        if list_items[item]["volumeInfo"].get("title") is not None:
            title=list_items[item]["volumeInfo"]["title"]
            book_info["title"]=title

            
        if list_items[item]["volumeInfo"].get("authors") is not None:
            author=list_items[item]["volumeInfo"]["authors"]
            book_info["author"]=author

        if list_items[item]["volumeInfo"].get("publisher") is not None:
            publisher=list_items[item]["volumeInfo"]["publisher"]
            book_info["publisher"]=publisher

        if list_items[item]["volumeInfo"].get("publishedDate") is not None:
            publishedDate=list_items[item]["volumeInfo"]["publishedDate"]
            book_info["publishedDate"]=publishedDate

        # if list_items[item]["volumeInfo"].get("description") is not None: 
        #     description=list_items[item]["volumeInfo"]["description"]
        #     book_info["description"]=description

        # if list_items[item].get("selfLink") is not None:  
        #     selfLink=list_items[item]["selfLink"]
        #     book_info["selfLink"]=selfLink

        
        if list_items[item]["volumeInfo"].get("imageLinks") is not None:
            imageLinks=list_items[item]["volumeInfo"]["imageLinks"]["thumbnail"]
            book_info["imageLinks"]=imageLinks
 
        short_item_list.append(book_info.copy())
        book_info.clear()
        # print(book_info)
        # print(short_item_list) 
    return render(request,'stores/searchedbooks.html',{'short_item_list':short_item_list,})
    # return JsonResponse(data,safe=False)
 

@login_required(login_url="/loginuser/")
def addInventory(request,book_id=None):  
    user=request.user
    if request.method=="POST" :   
        user_q=User.objects.get(username=user)
        book_id=request.POST['book_id']
        quantity=request.POST['quantity']
        # print(book_id)
        # print(quantity)
        Books.objects.create(user=user_q,book_id=book_id,number_of_copies=quantity)
        books=Books.objects.all().filter(user=user_q).values("book_id")
        # print(books)
        
        return HttpResponseRedirect("/Mystore/")
        # return render(request,"stores/Mystore.html",{'username':user})

    user_q=User.objects.get(username=user)
    book_q=Books.objects.filter(user=user_q,book_id=book_id)
    print("book_q:",book_q)

    if book_q.exists() :
        print(book_q," available")
        book_list=showbooks([book_id],user)
        book_info=book_list[0]
        return render(request,'stores/selectbook.html',{'book_info':book_info, })
 
    else : 
        book_list=showbooks([book_id])
        book_info=book_list[0]
         # return JsonResponse(book_info,safe=False)
        return render(request,'stores/selectbook.html',{'book_info':book_info, })


 

@login_required(login_url="/loginuser/")
def Mystore(request,book_id=None):
    user=request.user
    
    if request.method=="POST":
        user_q=User.objects.get(username=user)
        book=request.POST['book_id']
        quantity=request.POST['quantity']
        print("quantity :",quantity)
        book_q=Books.objects.get(user=user_q,book_id=book) #.update(number_of_copies= quantity)
        book_q.number_of_copies= quantity
        book_q.save()
        print("book_q:", book_q)
    

    if book_id is not None: 
        book_list=showbooks([book_id],user)
        book_info=book_list[0]
        return render(request,"stores/updateqty.html",{"book":book_info,})

    book_ids=Books.objects.all().filter(user=User.objects.get(username=user))
    book_list=showbooks(book_ids,user)
    # print(book_list)  
    return render(request,"stores/Mystore.html",{"books":book_list,})


def remove(request,book_id=None):
    user=request.user
    user_q=User.objects.get(username=user)
    book_q=Books.objects.get(user=user_q,book_id=book_id).delete()
    return HttpResponseRedirect("/Mystore/")
    # book_ids=Books.objects.all().filter(user=User.objects.get(username=user))
    # book_list=showbooks(book_ids,user)
    # return render(request,"stores/Mystore.html",{"books":book_list,})