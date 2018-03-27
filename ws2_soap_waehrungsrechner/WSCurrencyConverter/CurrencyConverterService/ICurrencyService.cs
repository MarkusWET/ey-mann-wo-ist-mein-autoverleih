using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.Serialization;
using System.ServiceModel;
using System.ServiceModel.Web;
using System.Text;

namespace CurrencyConverterService
{
    // NOTE: You can use the "Rename" command on the "Refactor" menu to change the interface name "IService1" in both code and config file together.
    [ServiceContract]
    public interface ICurrencyService
    {
        /// <summary>
        /// Enter amount to be converted to Euro, String format: 3 all caps letters (e.g. "USD")
        /// Currency Format: floating point number
        /// </summary>
        /// <param name="currOut"></param>
        /// <param name="amount"></param>
        /// <returns></returns>
        [OperationContract]
        decimal ConvertToEur(String currOut, decimal amount);

        /// <summary>
        /// Enter desired input and output currency, String format: 3 all caps letters (e.g. "USD")
        /// Currency Format: floating point number
        /// </summary>
        /// <param name="currIn"></param>
        /// <param name="currOut"></param>
        /// <param name="amount"></param>
        /// <returns></returns>
        /// 

        [OperationContract]
        decimal CrossConvert(String currIn, String currOut, decimal amount);

        // TODO: Add your service operations here
    }
}
