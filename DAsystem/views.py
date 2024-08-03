from django.shortcuts import render,redirect
from django.http import HttpResponse
from dafiles.models import File
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import io  # Import the io module

def get_dataframe(request):
    if 'file_id' in request.session:
        try:
            file_id = request.session['file_id']
            file_instance = File.objects.get(id=file_id)
            file_path = file_instance.file.path
            return pd.read_csv(file_path, sep=",")
        except File.DoesNotExist:
            return None
        except Exception as e:
            print(str(e))  # Print the exception for debugging
            return None
    return None


def homePage(request):
    if request.method=='POST':
        uploaded_file=request.FILES['file']
        
        try:
            file_instance =File(file=uploaded_file)
            file_instance .save()
            request.session['user']="True"

            # Store the file ID in the session
            request.session['file_id'] = file_instance.id

            file_path = file_instance.file.path

              # -------replacing all backward slash into forward slash in file path for execution of file------------
            #file_path = str(file_path).replace("\\", "/")
            # reading file  here--------------------------
            df = pd.read_csv(file_path, sep=",")
            

            # Convert the DataFrame to HTML
            df_html = df.to_html(classes="table table-striped")

            return render(request, "user/index.html",{'dataframe_html': df_html})
                    
        except Exception as e:
            print(str(e))  # Print the exception for debugging
            return HttpResponse("oops! something went wrong")
    return render(request, "index.html")



def userhome(request):
    if 'user' in request.session.keys():
        
        #     # reading file  here--------------------------
        df = get_dataframe(request)

        #     # Convert the DataFrame to HTML
        df_html = df.to_html(classes="table table-striped")

    
        return render(request, "user/index.html",{'dataframe_html': df_html})
    return render(request, "index.html")

def fileinfo(request):
    if 'user' in request.session.keys():
       
        #     # reading file  here--------------------------
        df = get_dataframe(request)
        

        # Get DataFrame information
        buffer = io.StringIO()
        df.info(buf=buffer)
        info_str = buffer.getvalue()
            
            # Convert DataFrame info to HTML
        info_html = '<pre>' + info_str + '</pre>'

        #     # Convert the DataFrame to HTML
        #df_html = info.to_html(classes="table table-striped")

    
        return render(request, "user/index.html",{'dataframe_html': info_html})
    return render(request, "index.html")
    


def filedesc(request):
    if 'user' in request.session.keys():
        
        #     # reading file  here--------------------------
        df = get_dataframe(request)
        desc=df.describe()
    

        #     # Convert the DataFrame to HTML
        df_html = desc.to_html(classes="table table-striped")

    
        return render(request, "user/index.html",{'dataframe_html': df_html})
    return render(request, "index.html")
    


def firstfive(request):
    if 'user' in request.session.keys():
       
        #     # reading file  here--------------------------
        df = get_dataframe(request)
        firstfive=df.head()
    

        #     # Convert the DataFrame to HTML
        df_html = firstfive.to_html(classes="table table-striped")

    
        return render(request, "user/index.html",{'dataframe_html': df_html})
    return render(request, "index.html")
    

def lastfive(request):
    if 'user' in request.session.keys():
       
        #     # reading file  here--------------------------
        df = get_dataframe(request)
        firstfive=df.tail()
    

        #     # Convert the DataFrame to HTML
        df_html = firstfive.to_html(classes="table table-striped")

    
        return render(request, "user/index.html",{'dataframe_html': df_html})
    return render(request, "index.html")
    


def isnull(request):
    if 'user' in request.session.keys():
    
        #     # reading file  here--------------------------
        df = get_dataframe(request)
        isnull=df.isnull()
        print(df.isnull())

        #     # Convert the DataFrame to HTML
        df_html = isnull.to_html(classes="table table-striped")

    
        return render(request, "user/index.html",{'dataframe_html': df_html})
    return render(request, "index.html")



def nullsum(request):
    if 'user' in request.session.keys():
    
        #     # reading file  here--------------------------
        df = get_dataframe(request)
        isnullsum=df.isnull().sum()
       
        # Convert Series to DataFrame for easier HTML rendering
        isnullsum_df = isnullsum.to_frame(name='Null Values').reset_index()
        isnullsum_df.columns = ['Column', 'Null Values']

        #     # Convert the DataFrame to HTML
        df_html = isnullsum_df.to_html(classes="table table-striped")

    
        return render(request, "user/index.html",{'dataframe_html': df_html})
    return render(request, "index.html")
    


def fillnull(request):
    if 'user' in request.session.keys():
    
        #     # reading file  here--------------------------
        df = get_dataframe(request)
        df.fillna(method="pad", inplace=True)
    
       
        #     # Convert the DataFrame to HTML
        df_html = df.to_html(classes="table table-striped")

    
        return render(request, "user/index.html",{'dataframe_html': df_html})
    return render(request, "index.html")
    


def showcolumns(request):
    if 'user' in request.session.keys():
    
        #     # reading file  here--------------------------
        df = get_dataframe(request)
        columns=df.columns.to_list()

         # Convert list of column names to HTML
        columns_html = "<ul>" + "".join(f"<li>{col}</li>" for col in columns) + "</ul>"

    
        return render(request, "user/index.html",{'dataframe_html': columns_html})
    return render(request, "index.html")
    


def statistic(request):
    if 'user' in request.session.keys():
    
        #     # reading file  here--------------------------
        df = get_dataframe(request)
         # Calculate mean, median, and standard deviation
        mean = df.mean(numeric_only=True)
        median = df.median(numeric_only=True)
        std_dev = df.std(numeric_only=True)
            
            # Convert the statistics to HTML
        stats_html = (
                "<h3>Mean</h3>" + mean.to_frame(name='Mean').reset_index().to_html(index=False, classes="table table-striped") +
                "<h3>Median</h3>" + median.to_frame(name='Median').reset_index().to_html(index=False, classes="table table-striped") +
                "<h3>Standard Deviation</h3>" + std_dev.to_frame(name='Standard Deviation').reset_index().to_html(index=False, classes="table table-striped")
            )
    
        return render(request, "user/index.html",{'dataframe_html': stats_html})
    return render(request, "index.html")
    

def scatterplot(request):
    if 'user' in request.session.keys():
        if request.method=="POST":
            x_axis=request.POST.get('x-axis')
            y_axis=request.POST.get('y-axis')
            df = get_dataframe(request)
            heading="Scatter Plot  Graph"
            try:
                if df is not None:
                    # Generate scatter plot
                    
                    plt.figure(figsize=(10, 6))
                    sns.scatterplot(data=df, x=x_axis, y=y_axis, hue='area_type', style='availability')
                    plt.title('Scatter Plot of ' + x_axis +" vs "+ y_axis)
                    plt.xlabel(x_axis)
                    plt.ylabel(y_axis)
                    plt.legend(loc='best')
                    # Save the plot
                    img_name=x_axis+y_axis+'scatterplot.png'
                    plot_path = 'static/img/'+img_name
                    plt.savefig(plot_path)
                    plt.close()
                    plot_path='img/'+img_name
                    
                    return render(request, "user/graphplot.html", {'plot_url': plot_path,'head_message':heading})
                return HttpResponse("No file found or an error occurred.")
            except:
                warning="Graph for these columns are not valid please try another"
                return render(request, "user/graphplot.html", {'warning_message':warning,'head_message':heading})
        return render(request, "user/graphplot.html")
    
    return render(request, "index.html")
    

def lineplot(request):
    if 'user' in request.session.keys():
        if request.method=="POST":
            x_axis=request.POST.get('x-axis')
            y_axis=request.POST.get('y-axis')
            df = get_dataframe(request)
            heading="Line Plot  Graph"
            try:
                if df is not None:
                    # Generate scatter plot
                   
                    # Ensure that the columns are numeric
                    df[x_axis] = pd.to_numeric(df[x_axis], errors='coerce')
                    df[y_axis] = pd.to_numeric(df[y_axis], errors='coerce')
                    
                    # Drop rows with NaN values in the columns used for plotting
                    df = df.dropna(subset=[x_axis, y_axis])
                    
                    plt.figure(figsize=(12, 8))
                    sns.lineplot(data=df, x=x_axis, y=y_axis, hue='area_type', style='availability', markers=True)
                    plt.title('Line Plot of ' + x_axis +" vs "+ y_axis)
                    plt.xlabel(x_axis)
                    plt.ylabel(y_axis)
                    plt.legend(loc='best')

                    
                    # Save the plot
                    img_name=x_axis+y_axis+'lineplot.png'
                    plot_path = 'static/img/'+img_name
                    plt.savefig(plot_path)
                    plt.close()
                    plot_path='img/'+img_name
                    
                    return render(request, "user/graphplot.html", {'plot_url': plot_path,'head_message':heading})
                return HttpResponse("No file found or an error occurred.")
            except:
                warning="Graph for these columns are not valid please try another"
                return render(request, "user/graphplot.html", {'warning_message':warning,'head_message':heading})

        return render(request, "user/graphplot.html")
    
    return render(request, "index.html")
    
    
    

def boxplot(request):
    if 'user' in request.session.keys():
        if request.method=="POST":
            x_axis=request.POST.get('x-axis')
            y_axis=request.POST.get('y-axis')
            df = get_dataframe(request)
            heading="Box Plot  Graph"
            try:
                if df is not None:
                    # Generate scatter plot
                
                    plt.figure(figsize=(12, 8))
                    sns.boxplot(data=df, x=x_axis, y=y_axis)
                    plt.title('Box Plot of ' + x_axis +" vs "+ y_axis)
                    plt.xlabel(x_axis)
                    plt.ylabel(y_axis)
                    
                    # Save the plot
                    img_name=x_axis+y_axis+'boxplot.png'
                    plot_path = 'static/img/'+img_name
                    plt.savefig(plot_path)
                    plt.close()
                    plot_path='img/'+img_name
                    
                    return render(request, "user/graphplot.html", {'plot_url': plot_path,'head_message':heading})
                return HttpResponse("No file found or an error occurred.")
            except:
                    warning="Graph for these columns are not valid please try another"
                    return render(request, "user/graphplot.html", {'warning_message':warning,'head_message':heading})
        return render(request, "user/graphplot.html")
    
    return render(request, "index.html")

def histogram(request):
    if 'user' in request.session.keys():
        if request.method == "POST":
            x_axis = request.POST.get('x-axis')
            y_axis = request.POST.get('y-axis')
            df = get_dataframe(request)
            heading = "Histogram Graph"
            
            try:
                if df is not None:
                    # Ensure the selected columns are numeric for histogram
                    df[x_axis] = pd.to_numeric(df[x_axis], errors='coerce')
                    df[y_axis] = pd.to_numeric(df[y_axis], errors='coerce')
                    
                    # Drop rows with NaN values in the selected columns
                    df = df.dropna(subset=[x_axis, y_axis])
                    
                    if df.empty:
                        warning = "No valid data for selected columns."
                        return render(request, "user/graphplot.html", {'warning_message': warning, 'head_message': heading})
                    
                    # Generate histogram plot
                    plt.figure(figsize=(12, 8))
                    plt.hist(df[x_axis], bins=20, color='blue', alpha=0.7)
                    plt.title('Histogram of ' + x_axis)
                    plt.xlabel(x_axis)
                    plt.ylabel('Frequency')
                    plt.grid(True)
                    
                    # Save the plot
                    img_name = x_axis + '_histogram.png'
                    plot_path = 'static/img/' + img_name
                    plt.savefig(plot_path)
                    plt.close()
                    plot_path = 'img/' + img_name
                    
                    return render(request, "user/graphplot.html", {'plot_url': plot_path, 'head_message': heading})
                
                return HttpResponse("No file found or an error occurred.")
            
            except KeyError:
                warning = "Selected columns are not valid. Please try another."
                return render(request, "user/graphplot.html", {'warning_message': warning, 'head_message': heading})
        
        return render(request, "user/graphplot.html")
    
    return render(request, "index.html")


def logout(request):
    request.session.flush()
    return redirect('homepage')
    






# if 'user' in request.session.keys():
#         df = get_dataframe(request)
#         if df is not None:
#             # Ensure that the columns are numeric
#             df['total_sqft'] = pd.to_numeric(df['total_sqft'], errors='coerce')
#             df['price'] = pd.to_numeric(df['price'], errors='coerce')
            
#             # Drop rows with NaN values in the columns used for plotting
#             df = df.dropna(subset=['total_sqft', 'price'])
            
#             plt.figure(figsize=(12, 8))
#             sns.lineplot(data=df, x='total_sqft', y='price', hue='area_type', style='availability', markers=True)
#             plt.title('Line Plot of Total Square Feet vs Price')
#             plt.xlabel('Total Square Feet')
#             plt.ylabel('Price')
#             plt.legend(loc='best')
            
#             # Save the plot
#             plot_path = 'static/img/lineplot.png'
#             plt.savefig(plot_path)
#             plt.close()
            
#             return render(request, "user/lineplot.html", {'plot_url': plot_path})
#         return HttpResponse("No file found or an error occurred.")
    
#     return render(request, "index.html")


# # if 'user' in request.session.keys():
# #         df = get_dataframe(request)
#         if df is not None:
#             plt.figure(figsize=(12, 8))
#             sns.boxplot(data=df, x='area_type', y='price')
#             plt.title('Box Plot of Price by Area Type')
#             plt.xlabel('Area Type')
#             plt.ylabel('Price')
            
#             # Save the plot
#             plot_path = 'static/img/boxplot.png'
#             plt.savefig(plot_path)
#             plt.close()
            
#             return render(request, "user/boxplot.html", {'plot_url': plot_path})
#         return HttpResponse("No file found or an error occurred.")
    
#     return render(request, "index.html")
    