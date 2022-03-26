import datetime

def stats_till_today(model, user, time_in_days=None):

    if(time_in_days == None):
        all_data_till_time = model.objects.filter(owner=user)
    else:
        todays_date = datetime.date.today()

        from_this_time = todays_date - datetime.timedelta(days=time_in_days)

        all_data_till_time = model.objects.filter(owner=user, 
                                date__gte = from_this_time, 
                                date__lte=todays_date)

    total_amount = 0

    for data in all_data_till_time:
        total_amount += data.amount
    
    return total_amount