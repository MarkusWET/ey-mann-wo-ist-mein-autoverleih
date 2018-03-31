# WebService 2 - Währungsrechner
 ```cs
        /// <summary>
        /// Enter amount to be converted to Euro, String format: 3 all caps letters (e.g. "USD")
        /// Currency Format: floating point number
        /// </summary>
        /// <param name="currOut"></param>
        /// <param name="amount"></param>
        /// <param name="auth"></param>
        /// <returns></returns>
        [OperationContract]
        decimal ConvertToEur(string currOut, string amount, string auth);

        /// <summary>
        /// Enter desired input and output currency, String format: 3 all caps letters (e.g. "USD")
        /// Currency Format: floating point number
        /// </summary>
        /// <param name="currIn"></param>
        /// <param name="currOut"></param>
        /// <param name="amount"></param>
        /// <param name="auth"></param>
        /// <returns></returns>
        /// 

        [OperationContract]
        decimal CrossConvert(string currIn, string currOut, string amount, string auth);
```
