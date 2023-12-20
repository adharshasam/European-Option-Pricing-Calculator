# installing essential libraries 

import tkinter as tk
from tkinter import *
from tkinter import ttk

import numpy as np
import math
import scipy
from scipy import stats
from scipy.stats import norm

# creating tkinter app window

root = tk.Tk()
root.title("European Option Pricing Calculator by Adharsha Sam")
root.geometry("940x640")

# function to calculate the call & put option prices using option pricing algorithms

option_var = tk.StringVar()
algo_var = tk.StringVar()

def calculate():

  option = option_var.get()
  algo = algo_var.get()
  iter = int(iter_entry.get())
  S0 = float(stockprice_entry.get())
  X = float(strikeprice_entry.get())
  T = float(tom_entry.get())
  rf = float(rf_entry.get())
  q = float(dividend_entry.get())
  sigma = float(volatility_entry.get())

  rf = round(rf/100, 2)
  q = round(q/100, 2)
  sigma = round(sigma/100, 2)

  # CASE 1: option = put & algo = bsm

  if option == "Put Option" and algo == "Black-Scholes Method": 
        d1 = (np.log(S0/X) + (rf - q + 0.5*sigma**2)*T)/(sigma * np.sqrt(T)) 
        d2 = d1 - sigma*np.sqrt(T) # risk-adjusted probability that the option will be exercised (strike > spot)
        P = X * np.exp(-rf * T)* norm.cdf(-d2) - S0 * np.exp(-q * T) * norm.cdf(-d1)
        C = P + S0 * np.exp(-q * T) - X * np.exp(-rf * T) # call option price using put-call parity
        callprice.config(text="Call Option Price: $%s" % round(C, 2))
        putprice.config(text="Put Option Price: $%s" % round(P, 2))

  # CASE 2: option = call & algo = mcs

  elif option == "Call Option" and algo == "Monte-Carlo Simulation": 
        np.random.seed(123) # to ensure reproducibility of results                                                           
        Z = np.random.normal(size = iter) # generates random variables that follow a normal distribution                                         
        St = S0 * np.exp((rf - q - sigma**2/2) * T) * np.exp(sigma * np.sqrt(T) * Z) # stock price at maturity
        ExpectedCallPayout = (1/iter) * np.sum(np.maximum(St - X, 0)) # expected call payout            
        C = ExpectedCallPayout * np.exp(-rf * T) # discounted call option price   
        P = C + X * np.exp(-rf * T) - S0 * np.exp(-q * T) # put option price using put-call parity
        callprice.config(text="Call Option Price: $%s" % round(C, 2))
        putprice.config(text="Put Option Price: $%s" % round(P, 2))

  # CASE 3: option = put & algo = mcs

  elif option == "Put Option" and algo == "Monte-Carlo Simulation": 
        np.random.seed(123) # to ensure reproducibility of results                                                            
        Z = np.random.normal(size = iter) # generates random variables that follow a normal distribution                                         
        St = S0 * np.exp((rf - q - sigma**2/2) * T) * np.exp(sigma * np.sqrt(T) * Z) # stock price at maturity
        ExpectedPutPayout = (1/iter) * np.sum(np.maximum(X - St, 0)) # expected put payout             
        P = ExpectedPutPayout * np.exp(-rf * T) # discounted put option price    
        C = P + S0 * np.exp(-q * T) - X * np.exp(-rf * T) # call option price using put-call parity
        callprice.config(text="Call Option Price: $%s" % round(C, 2))
        putprice.config(text="Put Option Price: $%s" % round(P, 2))

  # CASE 4: option = call & algo = bopm

  elif option == "Call Option" and algo == "Binomial Option Pricing Model": 
        
        def combination(N, i):
            return math.factorial(N)/(math.factorial(N - i) * math.factorial(i))

        dt = T/iter
        u = np.exp(sigma * np.sqrt(dt)) # upward movement factor           
        d = 1/u # downward movement factor                                   
        Pu = (np.exp((rf - q) * dt) - d)/(u - d) # risk-neutral probability of upward movement factor  
        Pd = 1 - Pu # risk-neutral probability of downward movement factor                               
        C = 0    
        for i in reversed(range(0, iter + 1)):
            St = S0 * u**i * d**(iter - i) # stock price at a specific binomial tree step                                  
            probability = combination(iter, i) * Pu**i * Pd**(iter - i) # upward/downward probability at a specific binomial tree step  
            C += probability * np.maximum(St - X, 0) # call option price at a specific binomial tree step                                        
        C = np.exp(-rf * T) * C  # discounted call option price          
        P = C + X * np.exp(-rf * T) - S0 * np.exp(-q * T) # put option price using put-call parity  
        callprice.config(text="Call Option Price: $%s" % round(C, 2))
        putprice.config(text="Put Option Price: $%s" % round(P, 2))

  # CASE 5: option = put & algo = bopm

  elif option == "Put Option" and algo == "Binomial Option Pricing Model": 
        
        def combination(N, i):
            return math.factorial(N)/(math.factorial(N - i) * math.factorial(i))
        
        dt = T/iter
        u = np.exp(sigma * np.sqrt(dt)) # upward movement factor           
        d = 1/u # downward movement factor                                   
        Pu = (np.exp((rf - q) * dt) - d)/(u - d) # risk-neutral probability of upward movement factor  
        Pd = 1 - Pu # risk-neutral probability of downward movement factor                               
        P = 0   
        for i in reversed(range(0, iter + 1)):
            St = S0 * u**i * d**(iter - i) # stock price at a specific binomial tree step                                   
            probability = combination(iter, i) * Pu**i * Pd**(iter - i) # upward/downward probability at a specific binomial tree step  
            P += probability * np.maximum(X - St, 0) # put option price at a specific binomial tree step                                        
        P = np.exp(-rf * T) * P  # discounted put option price        
        C = P + S0 * np.exp(-q * T) - X * np.exp(-rf * T) # call option price using put-call parity
        callprice.config(text="Call Option Price: $%s" % round(C, 2))
        putprice.config(text="Put Option Price: $%s" % round(P, 2))

  # CASE 6 (default settings): option = call & algo = bsm
  
  else: 
      d1 = (np.log(S0/X) + (rf - q + 0.5*sigma**2)*T)/(sigma * np.sqrt(T))
      d2 = d1 - sigma*np.sqrt(T) # risk-adjusted probability that the option will be exercised (spot > strike)
      C = np.exp(-q * T) * S0 * norm.cdf(d1) - X * np.exp(-rf * T) * norm.cdf(d2)
      P = C + X * np.exp(-rf * T) - S0 * np.exp(-q * T) # put option price using put-call parity
      callprice.config(text="Call Option Price: $%s" % round(C, 2))
      putprice.config(text="Put Option Price: $%s" % round(P, 2))
  
option_var.set("Call Option")
algo_var.set("Black-Scholes Method")

# creating app widgets

note0 = tk.Label(root, text = "", font = ("Rosewood Std Regular", 8, "italic"))
option_choice = tk.Label(root, text = "SELECT THE OPTION TYPE", font = ("Rosewood Std Regular", 10, "bold"), fg = "green")
drop1 = tk.OptionMenu(root, option_var, "Call Option", "Put Option")
note1 = tk.Label(root, text = "  (If call option is selected, the price of its corresponding put option will be calculated using Put-Call Parity & vice versa)", font = ("Rosewood Std Regular", 8, "italic"))
note00 = tk.Label(root, text = "", font = ("Rosewood Std Regular", 8, "italic"))

separator1 = ttk.Separator(root, orient = "horizontal")

note000 = tk.Label(root, text = "", font = ("Rosewood Std Regular", 8, "italic"))
algo_choice = tk.Label(root, text = "SELECT AN OPTION PRICING ALGORITHM", font = ("Rosewood Std Regular", 10, "bold"), fg = "green")
drop2 = tk.OptionMenu(root, algo_var, "Monte-Carlo Simulation", "Binomial Option Pricing Model", "Black-Scholes Method")
note0000 = tk.Label(root, text = "", font = ("Rosewood Std Regular", 8, "italic"))

separator2 = ttk.Separator(root, orient = "horizontal")

note00000 = tk.Label(root, text = "", font = ("Rosewood Std Regular", 8, "italic"))
itercount = tk.Label(root, text = "SET THE NUMBER OF ITERATIONS", font = ("Rosewood Std Regular", 10, "bold"), fg = "green")
iter_entry = tk.Entry(root, font=("Rosewood Std Regular", 10, "normal"))
note2 = tk.Label(root, text = "(For Monte-Carlo Simulation, please set max limit: 100000 simulations)", font = ("Rosewood Std Regular", 8, "italic"))
note3 = tk.Label(root, text = "(For Binomial Option Pricing Model, please set max limit: 1000 binomial tree time steps)", font = ("Rosewood Std Regular", 8, "italic"))
note4 = tk.Label(root, text = "    (For Black-Scholes Method, please set an arbitrary integer value since it is a Binomial Option Pricing Model with infinite time steps)", font = ("Rosewood Std Regular", 8, "italic"))
note000000 = tk.Label(root, text = "", font = ("Rosewood Std Regular", 8, "italic"))

separator3 = ttk.Separator(root, orient = "horizontal")

note0000000 = tk.Label(root, text = "", font = ("Rosewood Std Regular", 8, "italic"))
model_params = tk.Label(root, text = "ENTER MODEL PARAMETERS", font = ("Rosewood Std Regular", 10, "bold"), fg = "green")
note5 = tk.Label(root, text = "  (Please fill ALL these parameters with appropriate values)", font = ("Rosewood Std Regular", 8, "italic"))
note00000000 = tk.Label(root, text = "", font = ("Rosewood Std Regular", 8, "italic"))
  
stockprice_label1 = tk.Label(root, text = "Current Stock Price", font = ("Rosewood Std Regular", 10, "bold"))
stockprice_entry = tk.Entry(root, font=("Rosewood Std Regular", 10, "normal"))
stockprice_label2 = tk.Label(root, text = "USD", font = ("Rosewood Std Regular", 9))

strikeprice_label1 = tk.Label(root, text = "Strike Price", font = ("Rosewood Std Regular", 10, "bold"))
strikeprice_entry = tk.Entry(root, font = ("Rosewood Std Regular", 10, "normal"))
strikeprice_label2 = tk.Label(root, text = "USD", font = ("Rosewood Std Regular", 9))

tom_label1 = tk.Label(root, text = "Time to Maturity", font = ("Rosewood Std Regular", 10, "bold"))
tom_entry = tk.Entry(root, font = ("Rosewood Std Regular", 10, "normal"))
tom_label2 = tk.Label(root, text = "years", font = ("Rosewood Std Regular", 9))

rf_label1 = tk.Label(root, text = "Risk-free Rate", font = ("Rosewood Std Regular", 10, "bold"))
rf_entry = tk.Entry(root, font = ("Rosewood Std Regular", 10, "normal"))
rf_label2 = tk.Label(root, text = "%", font = ("Rosewood Std Regular", 9))

dividend_label1 = tk.Label(root, text = "Dividend Payout", font = ("Rosewood Std Regular", 10, "bold"))
dividend_entry = tk.Entry(root, font = ("Rosewood Std Regular", 10, "normal"))
dividend_label2 = tk.Label(root, text = "%", font = ("Rosewood Std Regular", 9))

volatility_label1 = tk.Label(root, text = "Volatility", font = ("Rosewood Std Regular", 10, "bold"))
volatility_entry = tk.Entry(root, font = ("Rosewood Std Regular", 10, "normal"))
volatility_label2 = tk.Label(root, text = "%", font = ("Rosewood Std Regular", 9))

note000000000 = tk.Label(root, text = "", font = ("Rosewood Std Regular", 8, "italic"))

separator4 = ttk.Separator(root, orient = "horizontal")

calc_button = tk.Button(root, text = "CALCULATE", command = calculate, font = ("Rosewood Std Regular", 10, "bold"), fg = "green", bg = "white")

results = tk.Label(root, text = "RESULTS", font = ("Rosewood Std Regular", 10, "bold"), fg = "green")
callprice = tk.Label(root, font = ("Rosewood Std Regular", 10, "bold"))
putprice = tk.Label(root, font = ("Rosewood Std Regular", 10, "bold"))

# organizing widgets using grid geometry manager

note0.grid(row = 0, column = 0)
option_choice.grid(row = 1, column = 0)
drop1.grid(row = 1, column = 1)
note1.grid(row = 2, column = 0)
note00.grid(row = 3, column = 0)

separator1.grid(row = 4, column = 0, sticky = "ew")

note000.grid(row = 5, column = 0)
algo_choice.grid(row = 6, column = 0)
drop2.grid(row = 6, column = 1)
note0000.grid(row = 7, column = 0)

separator2.grid(row = 8, column = 0, sticky = "ew")

note00000.grid(row = 9, column = 0)
itercount.grid(row = 10, column = 0)
iter_entry.grid(row = 11, column = 1)
note2.grid(row = 11, column = 0)
note3.grid(row = 12, column = 0)
note4.grid(row = 13, column = 0)
note000000.grid(row = 14, column = 0)

separator3.grid(row = 15, column = 0, sticky = "ew")

note0000000.grid(row = 16, column = 0)
model_params.grid(row = 17, column = 0)
note5.grid(row = 18, column = 0)
note00000000.grid(row = 19, column = 0)

stockprice_label1.grid(row = 20, column = 0)
stockprice_entry.grid(row = 20, column = 1)
stockprice_label2.grid(row = 20, column = 2)

strikeprice_label1.grid(row = 21, column = 0)
strikeprice_entry.grid(row = 21, column = 1)
strikeprice_label2.grid(row = 21, column = 2)

tom_label1.grid(row = 22, column = 0)
tom_entry.grid(row = 22, column = 1)
tom_label2.grid(row = 22, column = 2)

rf_label1.grid(row = 23, column = 0)
rf_entry.grid(row = 23, column = 1)
rf_label2.grid(row = 23, column = 2)

dividend_label1.grid(row = 24, column = 0)
dividend_entry.grid(row = 24, column = 1)
dividend_label2.grid(row = 24, column = 2)

volatility_label1.grid(row = 25, column = 0)
volatility_entry.grid(row = 25, column = 1)
volatility_label2.grid(row = 25, column = 2)

note000000000.grid(row = 26, column = 0)

separator4.grid(row = 27, column = 0, sticky = "ew")

calc_button.grid(row = 27, column = 1)

results.grid(row = 28, column = 0)
callprice.grid(row = 29, column = 0)
putprice.grid(row = 30, column = 0)

# infinite loop to run the app

root.mainloop()