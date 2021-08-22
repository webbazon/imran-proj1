if (localStorage.getItem('dataperiod') === null) { 
    localStorage.setItem('dataperiod', "all_time");
    document.write("All Time"); 
}
else {
    if (localStorage.getItem('dataperiod') === "all_time") { 
        document.write("All Time"); 
    } else if (localStorage.getItem('dataperiod') === "today") { 
        document.write("Today"); 
    } else if (localStorage.getItem('dataperiod') === "last_7_days") { 
        document.write("Last 7 Days"); 
    } else if (localStorage.getItem('dataperiod') === "last_30_days") { 
        document.write("Last 30 Days"); 
    } else if (localStorage.getItem('dataperiod') === "last_60_days") { 
        document.write("Last 60 Days"); 
    } else if (localStorage.getItem('dataperiod') === "last_90_days") { 
        document.write("Last 90 Days"); 
    } else if (localStorage.getItem('dataperiod') === "current_month") { 
        document.write("Current Month"); 
    } else if (localStorage.getItem('dataperiod') === "current_year") { 
        document.write("Current Year"); 
    } else if (localStorage.getItem('dataperiod') === "custom_period") { 
        document.write("Custom Period"); 
    }
}