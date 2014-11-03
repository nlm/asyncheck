from __future__ import absolute_import
import sys
import asyncheck
import nagplug

def check():
    np = nagplug.Plugin(version='1.0')
    np.add_arg('-p', '--port', metavar="port", default=26379, type=int, help="redis sentinel port")
    np.add_arg('-n', '--namespace', metavar="namespace", required=True, type=str, help="namespace to lookup")
    np.add_arg('-k', '--key', metavar="name", required=True, type=str, help="key to check")
    args = np.parse_args()
    np.set_timeout()
    se = asyncheck.RedisStorageEngine([(args.hostname, args.port)], args.namespace)
    result = se.get(args.key)
    if result is None:
        np.die("no result available")
    np.exit(code=result.code, message=result.message, perfdata=result.perfdata, extdata=result.extdata)

def push():
    np = nagplug.Plugin(version='1.0')
    np.add_arg('-p', '--port', metavar="port", default=26379, type=int, help="redis sentinel port")
    np.add_arg('-n', '--namespace', metavar="namespace", required=True, type=str, help="namespace to lookup")
    np.add_arg('-k', '--key', metavar="name", required=True, type=str, help="key to check")
    np.add_arg('-c', '--code', metavar="code", default=0, type=int, help="nagios status code: OK=0, WARNING=1, CRITICAL=2, UNKNOWN=3")
    np.add_arg('-m', '--message', metavar="message", default='', type=str, help="nagios status message")
    np.add_arg('-d', '--perfdata', metavar="perfdata", default='', type=str, help="nagios perf data")
    np.add_arg('-e', '--extdata', metavar="extdata", default='', type=str, help="nagios extended data")
    args = np.parse_args()
    np.set_timeout()
    se = asyncheck.RedisStorageEngine([(args.hostname, args.port)], args.namespace)
    if not se.set(args.key, asyncheck.Result(code=args.code, message=args.message)):
        sys.exit(1)

def delete():
    np = nagplug.Plugin(version='1.0')
    np.add_arg('-p', '--port', metavar="port", default=26379, type=int, help="redis sentinel port")
    np.add_arg('-n', '--namespace', metavar="namespace", required=True, type=str, help="namespace to lookup")
    np.add_arg('-k', '--key', metavar="name", required=True, type=str, help="key to check")
    args = np.parse_args()
    np.set_timeout()
    se = asyncheck.RedisStorageEngine([(args.hostname, args.port)], args.namespace)
    if not se.delete(args.key):
        sys.exit(1)
