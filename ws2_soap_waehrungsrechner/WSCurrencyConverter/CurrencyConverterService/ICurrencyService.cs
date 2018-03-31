using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.Serialization;
using System.ServiceModel;
using System.ServiceModel.Web;
using System.Text;

namespace CurrencyConverterService
{
    [ServiceContract]
    public interface ICurrencyService
    {
        /// <summary>
        /// Enter amount to be converted to Euro, as a string (american floating point notation)
        /// Currency Format: floating point number
        /// For currIn use ISO 4217 format
        /// </summary>
        /// <param name="currIn"></param>
        /// <param name="amount"></param>
        /// <param name="auth"></param>
        /// <returns></returns>
        [OperationContract]
        decimal ConvertToEur(string currIn, string amount, string auth);

        /// <summary>
        /// Enter desired input and output currency,
        /// money amount as a string (american floating point notation)
        /// For currIn and currOut use ISO 4217 format
        /// </summary>
        /// <param name="currIn"></param>
        /// <param name="currOut"></param>
        /// <param name="amount"></param>
        /// <param name="auth"></param>
        /// <returns></returns>
        /// 

        [OperationContract]
        decimal CrossConvert(string currIn, string currOut, string amount, string auth);

    }
}
