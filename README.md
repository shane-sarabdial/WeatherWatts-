# WeatherWatts-test test 3fdsfdsfsd
fdfd

base_score=0.5, booster='gbtree',
                                    n_estimators=8000,
                                    early_stopping_rounds=50,
                                    objective='reg:squarederror',
                                    max_depth=8,
                                    learning_rate=0.005,
                                    subsample = 0.7,
                                    reg_lambda = 5,
                                    min_child_weight =2,
                                    colsample_bytree = 0.8,
                                    random_state =0 --- cali




1849 lamda = 50



base_score=0.5, booster='gbtree',
                                    n_estimators=8000,
                                    early_stopping_rounds=50,
                                    max_depth=10,
                                    learning_rate=0.006,
                                    subsample = 0.8,
                                    reg_lambda = 60,
                                    min_child_weight =1,
                                    colsample_bytree = 0.8,
                                    colsample_level = 0.8,
                                    random_state =0,
                                    eval_metric =['rmse', 'mae']) - NY -1149, 749

  reg = xgb.XGBRegressor(base_score=0.5, booster='gbtree',
                                    n_estimators=8000,
                                    early_stopping_rounds=100,
                                    max_depth=10,
                                    learning_rate=0.006,
                                    subsample = 0.9,
                                    reg_lambda = 30,
                                    min_child_weight =1,
                                    colsample_bytree = 0.8,
                                    colsample_bylevel = 0.8,
                                    colsample_bynode = 0.7,
                                    random_state =0,
                                    eval_metric =['rmse', 'mae']) -ny 1039
  

reg = xgb.XGBRegressor(base_score=0.5, booster='gbtree',
                                    n_estimators=8000,
                                    early_stopping_rounds=100,
                                    max_depth=10,
                                    learning_rate=0.007,
                                    subsample = 0.9,
                                    reg_lambda = 15,
                                    min_child_weight =1,
                                    colsample_bytree = 0.8,
                                    colsample_bylevel = 0.8,
                                    colsample_bynode = 0.7,
                                    random_state =0,
                                    eval_metric =['rmse', 'mae'])-938 ny