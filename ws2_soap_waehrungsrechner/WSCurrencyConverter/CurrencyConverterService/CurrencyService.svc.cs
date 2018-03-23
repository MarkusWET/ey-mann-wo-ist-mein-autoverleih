using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Net;
using System.Runtime.Serialization;
using System.ServiceModel;
using System.ServiceModel.Web;
using System.Text;
using System.Xml;
using System.Xml.Linq;

namespace CurrencyConverterService
{
    // NOTE: You can use the "Rename" command on the "Refactor" menu to change the class name "CurrencyService" in code, svc and config file together.
    // NOTE: In order to launch WCF Test Client for testing this service, please select CurrencyService.svc or CurrencyService.svc.cs at the Solution Explorer and start debugging.
    public class CurrencyService : ICurrencyService
    {
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

        public decimal ConvertToEur(string currOut, decimal amount)
        {
            if (this.CurrencyData == null) SetCurrencyData();

            foreach (var item in CurrencyData)
            {
                if (item.Name.Equals(currOut)) return amount / item.Rate;
            }

            return 0;
        }

        public decimal CrossConvert(string currIn, string currOut, decimal amount)
        {
            //get intermediate value
            decimal temp = ConvertToEur(currIn, amount);

            foreach (var item in CurrencyData)
            {
                if (item.Name == currOut) return temp * item.Rate;
            }

            return 0;
        }
    }
}
