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

coin_report <- read_csv("C:/Users/aljackson/Documents/Environments/crypto_api/crypto_port.csv", col_types = cols(`Today's Price` = col_double(), 
                                                               `Market Value` = col_double(), `Today's Return` = col_double(), 
                                                               `Total Return` = col_double()))

coin_report_vars <- c('Crypto', 'Ticker', 'Avg Cost', 'Quantity')

coin_report <- coin_report[coin_report_vars]


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

today_date <- Sys.Date()

data_today <- coin_api[as.Date(as.POSIXct(coin_api$last_updated)) == today_date, ]

crypto_today <- data_today[data_today$symbol %in% as.vector(coin_report$Ticker), ]

# exclude golden-ratio-token

crypto_today <- crypto_today[!crypto_today$name %in% c('golden-ratio-token', 'unicorn-token', 'universe'),]

crypto_today_vars <- c('symbol', 'last_updated', 'price_usd')

crypto_price_today <- crypto_today[crypto_today_vars]

crypto_report <- merge(coin_report, crypto_price_today, by.x = 'Ticker', by.y = 'symbol', all.x = T)

# Add columns: "Market Value" , "Today's Return" , "Total Return"

crypto_report$market_value <- crypto_report$Quantity * crypto_report$price_usd
crypto_report$total_cost <- crypto_report$Quantity * crypto_report$`Avg Cost`

crypto_report$total_return <- crypto_report$market_value - crypto_report$total_cost
crypto_report$total_return_pct <- (crypto_report$market_value - crypto_report$total_cost) / crypto_report$total_cost

# order by total_return_pct desc

crypto_report <- crypto_report[order(-crypto_report$total_cost),]

total_df <- data.frame(Ticker = c('Total'),
                       Crypto = c('Alt Coins Above'),
                       `Avg Cost` = 0
                       , Quantity = 0
                       , last_updated = today_date
                       , price_usd = 0
                       , market_value = sum(crypto_report$market_value, na.rm=T)
                       , total_cost = sum(crypto_report$total_cost, na.rm=T)
                       , total_return = sum(crypto_report$total_return, na.rm=T)
                       , total_return_pct = 0)

total_df$total_return_pct <- (total_df$market_value - total_df$total_cost) / total_df$total_cost

names(total_df)[names(total_df) == "Avg.Cost"] <- "Avg Cost"

crypto_report <- rbind(crypto_report, total_df)

crypto_report$total_return_pct <- round((crypto_report$total_return_pct * 100), digits = 0)

write_csv(crypto_report, paste0('crypto_report_', today_date, '.csv'))
