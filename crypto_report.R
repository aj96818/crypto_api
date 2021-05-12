#install.packages("readr")
library(readr)

setwd('C:/Users/aljackson/Documents/Environments/crypto_api')

delete_date <- Sys.Date() - 8
#Define the file name that will be deleted
delete_fn <- paste0('crypto_report_', delete_date, '.csv')
#Check its existence
if (file.exists(delete_fn)) {
  #Delete file if it exists
  file.remove(delete_fn)
}

coin_port <- read_csv("C:/Users/aljackson/Documents/Environments/crypto_api/crypto_port.csv", col_types = cols(`Today's Price` = col_double(), 
      `Market Value` = col_double(), `Today's Return` = col_double(), 
      `Total Return` = col_double()))

coin_port_vars <- c('Crypto', 'Ticker', 'Avg Cost', 'Quantity')
coin_port <- coin_port[coin_port_vars]

coin_api <- read_csv("C:/Users/aljackson/Documents/Environments/crypto_api/CoinmarketcapAPI_Crypto_Data.csv", col_types = cols(symbol = col_character(),
      name = col_character(),
      date_added = col_datetime(format = ""),
      last_updated = col_datetime(format = ""),
      price_usd = col_double(),
      volume_24h = col_double(),
      market_cap = col_double(),
      percent_change_24h = col_double(),
      percent_change_7d = col_double(),
      percent_change_30d = col_double(),
      percent_change_60d = col_double(),
      percent_change_90d = col_double()))

coin_api <- coin_api[coin_api$symbol %in% as.vector(coin_port$Ticker), ]
coin_api <- coin_api[!coin_api$name %in% c('golden-ratio-token', 'unicorn-token', 'universe', 'stox'),]

today_date <- Sys.Date()
today_minus_180 <- as.vector(Sys.Date() - 180)
today_minus_365 <- as.vector(Sys.Date() - 365)

# create a vector of dates from 'last_updated' column:

date_vector <- as.vector(unique(as.Date(as.POSIXct(coin_api$last_updated, 'UTC'))))
close180 <- date_vector[which(abs(date_vector - today_minus_180)  == min(abs(date_vector - today_minus_180)))]
close365 <- ifelse(which(abs(date_vector - today_minus_180)  == min(abs(date_vector - today_minus_180))) == 0, Sys.Date() - 365,
                   date_vector[which(abs(date_vector - today_minus_365)  == min(abs(date_vector - today_minus_365)))])

t180_data <- coin_api[as.Date(as.POSIXct(coin_api$last_updated)) == close180, ]
t365_data <- coin_api[as.Date(as.POSIXct(coin_api$last_updated)) == close365, ]

data_today <- coin_api[as.Date(as.POSIXct(coin_api$last_updated)) == today_date, ]
crypto_today <- data_today[data_today$symbol %in% as.vector(coin_port$Ticker), ]

# Merge historical prices dataframes with current prices dataframe and eliminate columns that have all NA's.

merged_data <- merge(crypto_today, t180_data, by = 'symbol', all.x=T)
merged_data <- merge(merged_data, t365_data, by = 'symbol', all.x = T)
merged_data <- merged_data[,colSums(is.na(merged_data)) < nrow(merged_data)]

# Calculate percentage change in price for t180 & t360 time points if the price data exists.

merged_data$percent_change_180d <- (merged_data$price_usd.x - merged_data$price_usd.y) / merged_data$price_usd.y
merged_data$percent_change_365d <- (merged_data$price_usd.x - merged_data$price_usd) / merged_data$price_usd

merged_data$percent_change_180d <- round((merged_data$percent_change_180d * 100), digits = 0)
merged_data$percent_change_365d <- round((merged_data$percent_change_365d * 100), digits = 0)

# Keep only the variables of interest to clean up the report.

merged_data_vars <- c('symbol', 'name.x', 'last_updated.x', 'price_usd.x', 
                      'percent_change_24h.x', 'percent_change_7d.x', 'percent_change_30d.x',
                      'percent_change_60d.x', 'percent_change_90d.x', 'percent_change_180d',
                      'percent_change_365d')

merged_data <- merged_data[merged_data_vars]

# rename columns in coin_api report before joining to crypto_port (AJ's crypto portfolio)

colnames(merged_data) <- c('symbol', 'name', 'last_updated', 'price_usd', '24h', '7d', 
                           '30d', '60d', '90d', '180d', '365d')

merged_data$`24h` <- round(merged_data$`24h`, digits = 0)
merged_data$`7d` <- round(merged_data$`7d`, digits = 0)
merged_data$`30d` <- round(merged_data$`30d`, digits = 0)
merged_data$`60d` <- round(merged_data$`60d`, digits = 0)
merged_data$`90d` <- round(merged_data$`90d`, digits = 0)

crypto_report <- merge(coin_port, merged_data, by.x = 'Ticker', by.y = 'symbol', all.x = T)

# Add columns: "Market Value" , "Today's Return" , "Total Return"

crypto_report$market_value <- crypto_report$Quantity * crypto_report$price_usd
crypto_report$total_cost <- crypto_report$Quantity * crypto_report$`Avg Cost`
crypto_report$total_return <- crypto_report$market_value - crypto_report$total_cost
crypto_report$total_return_pct <- (crypto_report$market_value - crypto_report$total_cost) / crypto_report$total_cost

# order by total_return_pct desc

crypto_report <- crypto_report[order(-crypto_report$total_return),]

total_df <- data.frame(Ticker = c('Total'),
                       Crypto = c('Alt Coins Above'),
                       `Avg Cost` = 0
                       , Quantity = 0
                       , name = ''
                       , last_updated = today_date
                       , price_usd = 0
                       , `24h` = round(mean(crypto_report$`24h`, na.rm = T), digits = 0)
                       , `7d` = round(mean(crypto_report$`7d`, na.rm = T), digits = 0)
                       , `30d` = round(mean(crypto_report$`30d`, na.rm = T), digits = 0)
                       , `60d` = round(mean(crypto_report$`60d`, na.rm = T), digits = 0)
                       , `90d` = round(mean(crypto_report$`90d`, na.rm = T), digits = 0)
                       , `180d` = round(mean(crypto_report$`180d`, na.rm = T), digits = 0)
                       , `365d` = round(mean(crypto_report$`365d`, na.rm = T), digits = 0)
                       , market_value = sum(crypto_report$market_value, na.rm=T)
                       , total_cost = sum(crypto_report$total_cost, na.rm=T)
                       , total_return = sum(crypto_report$total_return, na.rm=T)
                       , total_return_pct = 0)

total_df$total_return_pct <- (total_df$market_value - total_df$total_cost) / total_df$total_cost

names(total_df)[names(total_df) == "Avg.Cost"] <- "Avg Cost"

colnames(total_df) <- c('Ticker', 'Crypto', 'Avg Cost', 'Quantity', 'name', 'last_updated'
                        , 'price_usd', '24h', '7d', '30d', '60d', '90d', '180d', '365d'
                        , 'market_value', 'total_cost', 'total_return', 'total_return_pct')

crypto_report <- rbind(crypto_report, total_df)

crypto_report$total_return_pct <- round((crypto_report$total_return_pct * 100), digits = 0)
crypto_report$price_usd <- round(crypto_report$price_usd, digits = 2)
crypto_report$market_value <- round(crypto_report$market_value, digits = 2)
crypto_report$total_cost <- round(crypto_report$total_cost, digits = 2)
crypto_report$total_return <- round(crypto_report$total_return, digits = 2)

write_csv(crypto_report, paste0('crypto_report_', today_date, '.csv'))
