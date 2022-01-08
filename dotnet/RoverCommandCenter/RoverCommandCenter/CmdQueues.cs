using System.Collections.Concurrent;

namespace RoverCommandCenter
{
    public static class CmdQueues
    {

        public static ConcurrentDictionary<string, ConcurrentQueue<string>> Queues { get; set; } = new();


        public static void PostCmd(string rover, string command)
        {
            if (!Queues.ContainsKey(rover))
            {
                Queues[rover] = new ConcurrentQueue<string>();
            }

            Queues[rover].Enqueue(command);
        }

        public static string GetCmd(string rover)
        {
            if (Queues.ContainsKey(rover))
            {
                if (Queues[rover].TryDequeue(out string? command))
                {
                    if (command != null)
                        return command;
                }
            }

            return "";
        }

    }
}
