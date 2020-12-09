from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from alpha_vantage.timeseries import TimeSeries
from datetime import date
from . import models


def must_be_unique(value):
    user = User.objects.filter(email=value)
    if len(user) > 0:
        raise forms.ValidationError("Email Already in Use")
    return value


# Class used by PitchCreator
class PostPitchForm(forms.ModelForm):

    # meta class
    class Meta:
        # model to be used
        model = models.UserModel
        # fields to be used
        fields = [
            "header",
            "post",
            "cost",
        ]
    def save(self, request):
        post_instance = models.UserModel()
        post_instance.post = self.cleaned_data["post"]
        post_instance.author = request.user
        post_instance.header = self.cleaned_data["header"]
        post_instance.cost = self.cleaned_data["cost"]
        post_instance.save()
        return post_instance

# Class used by CommentCreator
class PostCommentForm(forms.ModelForm):

    # meta class
    class Meta:
        # model to be used
        model = models.CommentModel
        # fields to be used
        fields = [
           "comment",
        ]
    def save(self, request, pk):
        post_instance = models.UserModel.objects.get(id=pk)
        comment_instance = models.CommentModel()
        comment_instance.post = post_instance
        comment_instance.comment = self.cleaned_data["comment"]
        comment_instance.author = request.user
        comment_instance.save()
        return comment_instance

class AddFundsForm(forms.ModelForm):

    # meta class
    class Meta:
        # model to be used
        model = models.CatcherModel
        # fields to be used
        fields = [
           "funds",
        ]


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        label="Email",
        required=True,
        validators=[must_be_unique]
    )

    class Meta:
        model = User
        fields = ("username", "email",
                  "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class AddStocksForm(forms.ModelForm):
    
    class Meta:
        model = models.StocksModel
        fields = [
            "ticker",
            "date",
            "closingPrice",
            "percentageChange"
        ]

    def save(self, request):
        ts = TimeSeries(key="VLG4S2J38MECAW2U", output_format='pandas')
        # Check if stock already in DB
        #   if yes, get_daily with compact output_size

        # brand new stock
        # Check stock exists and get data
        try:
            data = ts.get_daily(symbol=self.cleaned_data["ticker"], outputsize='full')
            stock = models.StocksModel()
            stock.ticker = self.cleaned_data["ticker"]
            stock.date = data['date'][-1] # last day in data
            stock.closingPrice = data['4. close'][-1] # last closing price
            stock.percentageChange = data['4. close'][-1].pct_change() # last closing price in percent change
        except:
            print("Ticker doesn't exist") # ts fails or stock doesn't exist


class AddTrackedStocksForm(forms.ModelForm):
    
    class Meta:
        model = models.TrackedStocksModel
        fields = [
            "ticker",
            "description",
            "category"
        ]

    def save(self, request, pk):
        trackedStock = models.TrackedStockModel()
        trackedStock.pitcher = request.user
        trackedStock.description = self.cleaned_data["description"]
        trackedStock.category = self.cleaned_data["category"]
        trackedStock.ticker = self.cleaned_data["ticker"]
        ts = TimeSeries(key="VLG4S2J38MECAW2U", output_format='pandas')
        try:
            obj = models.StocksModel.objects.get(ticker=trackedStock.ticker, date=date.today())
            trackedStock.data = obj
        except:
            try:
                data = ts.get_daily(symbol=trackedStock.ticker, outputsize='compact')
                obj2 = models.StocksModel.objects.get(ticker=trackedStock.ticker)

            except:
            #data['4. close'][-1] last closing price
            #data['4. close'][-1].pct_change() # last closing price in percent change
                itor = None
                while itor != date.today():
                    models.StocksModel.objects.create(ticker=trackedStock.ticker, date=date.today(), closingPrice=data['4. close'][-1], percentageChange=data['4. close'][-1].pct_change())
                    itor = 
        
        
        # Check if StocksModel of self.cleaned_data["ticker"] already exists
        #   if it exists
        #       make sure StocksModel is updated to last closing price, using outputsize='compact'
        #       set TrackedStock.data to StocksModel
        #   if it doesn't exist
        #       create new StocksModel with outputsize='full'
        #       set TrackedStock.data to StocksModel