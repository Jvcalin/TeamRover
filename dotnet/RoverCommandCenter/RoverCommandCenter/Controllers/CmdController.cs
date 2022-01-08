using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;

namespace RoverCommandCenter
{
    [Route("api/[controller]")]
    [ApiController]
    public class CmdController : ControllerBase
    {

        // GET api/cmd/roger
        [HttpGet("{id}")]
        public string Get(string id)
        {
            return CmdQueues.GetCmd(id);
        }

        // POST api/cmd/roger
        [HttpPost("{id}")]
        public void Post(string id, [FromBody] string value)
        {
            CmdQueues.PostCmd(id, value);
        }
    }
}
