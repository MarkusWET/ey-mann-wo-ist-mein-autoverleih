using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Net;
using System.Timers;
using System.Xml.Linq;
using System.Globalization;
using System.Security.Cryptography;
using System.Text;

namespace CurrencyConverterService
{
    public class CurrencyService : ICurrencyService
    {
        string hashedKey = sha256("CorrectHorseBatteryStaple");

        public List<Currency> CurrencyData { get; set; }

        private void SetCurrencyData()
        {
            //variable for holding the xml as a string
            string xmlString;

            //the using statement takes care of creating and disposing a file reader to read the xml from the web
            using (WebClient client = new WebClient())
            {
                xmlString = client.DownloadString("http://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml");
            }

            //An XDocument object (which is queryable by LINQ is created from the string
            XDocument xDocument = XDocument.Load(new StringReader(xmlString));

            // The namespace needs to be specified in order to be able to query the cube items which contain the currency data
            var ns = (XNamespace)"http://www.ecb.int/vocabulary/2002-08-01/eurofxref";

            //With the use of a LINQ query and lambda expressions a List containing currency objects is created
            var currencies = xDocument
                .Root
                .Element(ns + "Cube")
                .Element(ns + "Cube")
                .Elements(ns + "Cube")
                .Select(xElement => new Currency
                {
                    Name = (string)xElement.Attribute("currency"),
                    Rate = (decimal)xElement.Attribute("rate")
                })
                .ToList();

            this.CurrencyData = currencies;
        }

        private decimal ConvertToEur(string currOut, string amount)
        {
            try
            {
                decimal amountParsed = ParseDecimal(amount);

                if (this.CurrencyData == null)
                    SetCurrencyData();

                foreach (var item in CurrencyData)
                {
                    if (item.Name.Equals(currOut))
                        return amountParsed / item.Rate;
                }

                return -1;
            }
            catch (Exception)
            {
                return -1;
            }
        }

        private static decimal ParseDecimal(string strIn)
        {
            decimal decOut;
            Decimal.TryParse(strIn, NumberStyles.AllowDecimalPoint, new CultureInfo("en-EN"), out decOut);
            return decOut;
        }

        /// <summary>
        /// taken from: https://stackoverflow.com/questions/12416249/hashing-a-string-with-sha256
        /// </summary>
        /// <param name="randomString"></param>
        /// <returns></returns>
        static string sha256(string randomString)
        {
            var crypt = new SHA256Managed();
            string hash = String.Empty;
            byte[] crypto = crypt.ComputeHash(Encoding.UTF8.GetBytes(randomString));
            foreach (byte theByte in crypto)
            {
                hash += theByte.ToString("x2");
            }
            return hash;
        }

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
        public decimal ConvertToEur(string currOut, string amount, string auth)
        {
            if (!hashedKey.Equals(auth))
                return -1;

            currOut = currOut.ToUpper();


            return ConvertToEur(currOut, amount);
        }



        /// <summary>
        /// Enter desired input and output currency, String format: 3 all caps letters (e.g. "USD")
        /// Currency Format: floating point number
        /// </summary>
        /// <param name="currIn"></param>
        /// <param name="currOut"></param>
        /// <param name="amount"></param>
        /// <returns></returns>
        public decimal CrossConvert(string currIn, string currOut, string amount, string auth)
        {
            if (!hashedKey.Equals(auth))
                return -1;

            currIn = currIn.ToUpper();
            currOut = currOut.ToUpper();

            Decimal temp;

            //get intermediate value
            if (currIn.Equals("EUR"))
            {
                temp = ParseDecimal(amount);
                SetCurrencyData();
            }
            else
            {
                temp = ConvertToEur(currIn, amount);
            }

            foreach (var item in CurrencyData)
            {
                if (item.Name == currOut)
                    return temp * item.Rate;
            }

            return 0;
        }


    }
}
