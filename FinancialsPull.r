library(quantmod)

#pick the companies to pull data for
fin <- c('GOOGL','AAPL','AMZN','EBAY','CRM','FB','PG','MMM')

#function to iterate through the companies, and mark companies that returned errors with NULL
getFin_HANDLED <- function (symb) {
    return(tryCatch(getFin(symb,auto.assign = "FALSE"), error = function(e) NULL))
 }

#iterate through the vector of companies
fin.f <- lapply(fin, getFin_HANDLED)

#name companies according to the elements of the company vector
names(fin.f) <- fin

#extract companies that returned an error
fin.n <- names(fin.f[sapply(fin.f, is.null)])
#keep companies that did not return an error
fin.f <- fin.f[!sapply(fin.f, is.null)]

save(fin.f,file = "fin_f.RData")

#fin.f is arranged as [["Company"]][["Financial Statement"]][["Quarter or Annual"]][["Individual Element"]]
#Financial Statment levels: 1 = Income Statment, 2 = Balance Sheet, 3 = Cash Flow statement
#Quarterly or Annual levels: 1 = End of Quarter, 2 = Annual (maximum 4 periods prior)
#Individual Element levels: 1 = Revenue on Income Statement and so on.


#iterate through fin.f and build a list of the annual income statements
IS_list <- lapply(names(fin.f), function (x) assign(paste(x, "IS", sep = "_"), as.data.frame(fin.f[[x]][[1]][[2]]) ))
names(IS_list) <- names(fin.f)
IS_list <- lapply(IS_list, rev)﻿

#iterate through fin.f and build a list of the annual Balance Sheets
BS_list <- lapply(names(fin.f), function (x) assign(paste(x, "BS", sep = "_"), as.data.frame(fin.f[[x]][[2]][[2]]) ))
names(BS_list) <- names(fin.f)
BS_list <- lapply(BS_list, rev)

#iterate through fin.f and build a list of the annual Cash Flow Statements
CF_list <- lapply(names(fin.f), function (x) assign(paste(x, "CF", sep = "_"), as.data.frame(fin.f[[x]][[3]][[2]]) ))
names(CF_list) <- names(fin.f)
CF_list <- lapply(CF_list, rev)

( BS_list[["AAPL"]][[1,4]] - BS_list[["AAPL"]][[1,3]])
# returns [1] 2868
( CF_list[["AAPL"]][[17,4]] )
# returns [1] -195

#Current Assets - Current Liabilities
(BS_list[["AAPL"]][[9,4]] - BS_list[["AAPL"]][[22,4]])
