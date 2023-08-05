import functools
import string
from collections import defaultdict
from pathlib import Path
from random import Random
from typing import *

from orkestra.interfaces import (
    Duration,
    Runtime,
    LambdaInvocationType,
    IntegrationPattern,
)
from orkestra.utils import coerce

OptionalFn = Optional[Union[Callable, Iterable[Callable]]]

random = Random(0)

_id_map = defaultdict(lambda: 1)


def _sample(k=4):
    return "".join(random.sample(string.hexdigits, k))


def _incremental_id(id):

    mapped = _id_map[id]

    result = id if mapped == 1 else f"{id}{mapped}"

    _id_map[id] += 1

    return result


class Compose:
    def __init__(
        self,
        func: OptionalFn = None,
        powertools: bool = False,
        log_event=True,
        capture_response=True,
        capture_error=True,
        raise_on_empty_metrics=False,
        capture_cold_start_metric=True,
        default_dimentions=None,
        model=None,
        envelope=None,
        timeout: Optional[Duration] = None,
        is_map_job: bool = False,
        runtime: Optional[Runtime] = None,
        comment: Optional[str] = None,
        input_path: Optional[str] = None,
        items_path: Optional[str] = None,
        max_concurrency: Optional[Union[int, float, None]] = None,
        output_path: Optional[str] = None,
        parameters: Optional[Mapping[str, Any]] = None,
        result_path: Optional[str] = None,
        result_selector: Optional[Mapping[str, any]] = None,
        client_context: Optional[str] = None,
        invocation_type: Optional[LambdaInvocationType] = None,
        payload_response_only: Optional[bool] = None,
        qualifier: Optional[str] = None,
        retry_on_service_exceptions: Optional[bool] = None,
        heartbeat: Optional[Duration] = None,
        integration_pattern: Optional[IntegrationPattern] = None,
        sfn_timeout: Optional[Duration] = None,
        **aws_lambda_constructor_kwargs,
    ):
        """
        Container for functions meant to be composed.

        Args:
            func: a function or list or tuple of functions
            timeout: the timeout duration of the lambda
            powertools: if true, enables powertools
            log_event: passed to aws_lambda_powertools.Logger
            capture_response: passed to aws_lambda_powertools.Tracer
            capture_error: passed to aws_lambda_powertools.Tracer
            raise_on_empty_metrics: passed to aws_lambda_powertools.Metrics
            capture_cold_start_metric: passed to aws_lambda_powertools.Metrics
            default_dimentions: passed to aws_lambda_powertools.Metrics
            model: passed to aws_lambda_powertools.utilities.parser.event_parser
            envelope: passed to aws_lambda_powertools.utilities.parser.event_parser
            runtime: the python runtime to use for the lambda
            is_map_job: whether the lambda is a map job
            comment: An optional description for this state. Default: No comment
            input_path: JSONPath expression to select part of the state to be the input to this state. May also be the special value JsonPath.DISCARD, which will cause the effective input to be the empty object {}. Default: $
            items_path:  JSONPath expression to select the array to iterate over. Default: $
            max_concurrency: MaxConcurrency. An upper bound on the number of iterations you want running at once. Default: - full concurrency
            output_path: JSONPath expression to select part of the state to be the output to this state. May also be the special value JsonPath.DISCARD, which will cause the effective output to be the empty object {}. Default: $
            parameters: The JSON that you want to override your default iteration input. Default: $
            result_path: JSONPath expression to indicate where to inject the state’s output. May also be the special value JsonPath.DISCARD, which will cause the state’s input to become its output. Default: $
            result_selector: The JSON that will replace the state’s raw result and become the effective result before ResultPath is applied. You can use ResultSelector to create a payload with values that are static or selected from the state’s raw result. Default: - None
            client_context: Up to 3583 bytes of base64-encoded data about the invoking client to pass to the function. Default: - No context
            invocation_type: Invocation type of the Lambda function. Default: InvocationType.REQUEST_RESPONSE
            payload_response_only: Invoke the Lambda in a way that only returns the payload response without additional metadata. The payloadResponseOnly property cannot be used if integrationPattern, invocationType, clientContext, or qualifier are specified. It always uses the REQUEST_RESPONSE behavior. Default: false
            qualifier:  Version or alias to invoke a published version of the function. You only need to supply this if you want the version of the Lambda Function to depend on data in the state machine state. If not, you can pass the appropriate Alias or Version object directly as the lambdaFunction argument. Default: - Version or alias inherent to the lambdaFunction object.
            retry_on_service_exceptions: Whether to retry on Lambda service exceptions. This handles Lambda.ServiceException, Lambda.AWSLambdaException and Lambda.SdkClientException with an interval of 2 seconds, a back-off rate of 2 and 6 maximum attempts. Default: true
            heartbeat: Timeout for the heartbeat. Default: - None
            integration_pattern: AWS Step Functions integrates with services directly in the Amazon States Language. You can control these AWS services using service integration patterns Default: IntegrationPattern.REQUEST_RESPONSE
            sfn_timeout: Timeout for the state machine. Default: - None
            **aws_lambda_constructor_kwargs: pass directly to sfn.PythonFunction

        For cdk params see https://docs.aws.amazon.com/cdk/api/latest/python/modules.html
        For powertools params see https://awslabs.github.io/aws-lambda-powertools-python/latest/
        """

        self.func = func
        self.runtime = runtime
        self.downstream = []

        self.timeout = timeout

        self.is_map_job = is_map_job

        self.aws_lambda_constructor_kwargs = aws_lambda_constructor_kwargs

        self.map_job_kwargs = {
            "comment": comment,
            "input_path": input_path,
            "items_path": items_path,
            "max_concurrency": max_concurrency,
            "output_path": output_path,
            "result_path": result_path,
            "result_selector": result_selector,
            "parameters": parameters,
        }

        self.lambda_invoke_kwargs = {
            "client_context": client_context,
            "invocation_type": invocation_type,
            "payload_response_only": payload_response_only,
            "retry_on_service_exceptions": retry_on_service_exceptions,
            "heartbeat": heartbeat,
            "integration_pattern": integration_pattern,
            "timeout": sfn_timeout,
            "comment": comment,
            "input_path": input_path,
            "output_path": output_path,
            "result_path": result_path,
            "result_selector": result_selector,
            "qualifier": qualifier,
        }

        if func and not isinstance(func, (list, tuple)):

            module = func.__module__.split(".")

            self.entry = str(Path(*module).parent)
            self.index = Path(*module).name + ".py"
            self.handler = func.__name__

        if powertools:
            self.__call__ = enable_powertools(
                decorated=self.__call__,
                log_event=log_event,
                capture_error=capture_error,
                capture_response=capture_response,
                capture_cold_start_metric=capture_cold_start_metric,
                raise_on_empty_metrics=raise_on_empty_metrics,
                default_dimentions=default_dimentions,
                model=model,
                envelope=envelope,
            )

    def __call__(self, event, context=None):

        if isinstance(self.func, (list, tuple)):

            raise TypeError("can't call a list of functions")

        if self.func is not None:

            return self.func(event, context)

        else:

            func = event

            return Compose(
                func=func,
                timeout=self.timeout,
                is_map_job=self.is_map_job,
                **self.aws_lambda_constructor_kwargs,
            )

    def __repr__(self) -> str:

        if isinstance(self.func, (list, tuple)):
            func = repr(self.func)
        else:
            func = self.func.__name__ if self.func is not None else None

        return (
            "Task("
            f"func={func}, "
            f"aws_lambda_constructor_kwargs={self.aws_lambda_constructor_kwargs}, "
            f"len_downstream={len(self.downstream)}"
            ")"
        )

    def __rshift__(self, right):
        right = (
            Compose(func=right) if isinstance(right, (list, tuple)) else right
        )
        self.downstream.append(right)
        return right

    @staticmethod
    def _render_lambda(
        composable: "Compose",
        scope,
        id=None,
        function_name=None,
        tracing=None,
        runtime=None,
        dead_letter_queue_enabled=False,
        **kwargs,
    ):

        from aws_cdk import aws_lambda, aws_lambda_python

        tracing = tracing or aws_lambda.Tracing.ACTIVE
        runtime = runtime or aws_lambda.Runtime.PYTHON_3_8

        keyword_args = dict(
            entry=composable.entry,
            handler=composable.handler,
            index=composable.index,
            function_name=function_name,
            runtime=runtime,
            tracing=tracing,
            dead_letter_queue_enabled=dead_letter_queue_enabled,
        )

        keyword_args.update(kwargs)

        keyword_args.update(composable.aws_lambda_constructor_kwargs)

        id = id or f"{composable.func.__name__}_fn_{_sample()}"

        if composable.timeout is not None:

            keyword_args.update(timeout=composable.timeout.construct)

        if composable.runtime is not None:

            keyword_args.update(runtime=composable.runtime.construct)

        return aws_lambda_python.PythonFunction(
            scope,
            id,
            **keyword_args,
        )

    def aws_lambda(
        self,
        scope,
        id=None,
        function_name=None,
        tracing=None,
        runtime=None,
        dead_letter_queue_enabled=False,
        **kwargs,
    ):

        return self._render_lambda(
            self,
            scope,
            id=id,
            function_name=function_name,
            tracing=tracing,
            runtime=runtime,
            dead_letter_queue_enabled=dead_letter_queue_enabled,
            **kwargs,
        )

    def task(
        self,
        scope,
        id=None,
        payload_response_only=True,
        function_name=None,
        **kwargs,
    ):

        from aws_cdk import aws_stepfunctions as sfn
        from aws_cdk import aws_stepfunctions_tasks as sfn_tasks

        if self.is_map_job:

            id = id or _incremental_id(self.func.__name__)

            map_kwargs = dict(id=id)

            map_kwargs.update(
                {k: v for k, v in self.map_job_kwargs.items() if v is not None}
            )

            task = sfn.Map(scope, **map_kwargs)

            lambda_fn = self.aws_lambda(
                scope,
                function_name=function_name,
            )

            keyword_args = dict(
                lambda_function=lambda_fn,
                payload_response_only=payload_response_only,
            )

            keyword_args.update(
                {
                    k: v
                    for k, v in self.lambda_invoke_kwargs.items()
                    if v is not None
                }
            )

            invoke_lambda = sfn_tasks.LambdaInvoke(
                scope,
                f"invoke_{id}",
                **keyword_args,
            )

            task.iterator(invoke_lambda)

        elif not isinstance(self.func, (list, tuple)):

            id = id or _incremental_id(self.func.__name__)

            lambda_fn = self.aws_lambda(
                scope,
                function_name=function_name,
            )

            keyword_args = dict(
                lambda_function=lambda_fn,
                payload_response_only=payload_response_only,
            )

            keyword_args.update(kwargs)

            keyword_args.update(
                {
                    k: v
                    for k, v in self.lambda_invoke_kwargs.items()
                    if v is not None
                }
            )

            task = sfn_tasks.LambdaInvoke(
                scope,
                id,
                **keyword_args,
            )

        else:

            task = sfn.Parallel(
                scope,
                "parallelize {}".format([c.func.__name__ for c in self.func]),
            )

            for fn in self.func:

                lambda_fn = fn.aws_lambda(scope)

                keyword_args = dict(
                    lambda_function=lambda_fn,
                    payload_response_only=payload_response_only,
                )

                keyword_args.update(kwargs)

                keyword_args.update(
                    {
                        k: v
                        for k, v in self.lambda_invoke_kwargs.items()
                        if v is not None
                    }
                )

                branch = sfn_tasks.LambdaInvoke(
                    scope,
                    _incremental_id(fn.func.__name__),
                    **keyword_args,
                )

                if isinstance(self.func, tuple):

                    branch.add_catch(
                        sfn.Pass(scope, f"{fn.func.__name__}_failed")
                    )

                task.branch(branch)

        return coerce(task)

    def definition(
        self,
        scope,
        definition=None,
    ):

        task = self.task(scope)

        definition = task if definition is None else definition.next(task)

        if self.downstream:
            for c in self.downstream:
                c.definition(scope, definition=definition)

        return definition

    def state_machine(
        self,
        scope,
        id=None,
        tracing_enabled=True,
        state_machine_name=None,
        **kwargs,
    ):

        from aws_cdk import aws_stepfunctions as sfn

        id = id or f"{self.func.__name__}_sfn_{_sample()}"

        return sfn.StateMachine(
            scope,
            id,
            definition=self.definition(scope),
            tracing_enabled=tracing_enabled,
            state_machine_name=state_machine_name,
            **kwargs,
        )

    def schedule(
        self,
        scope,
        id=None,
        expression: Optional[str] = None,
        day: Optional[str] = None,
        hour: Optional[str] = None,
        minute: Optional[str] = None,
        month: Optional[str] = None,
        week_day: Optional[str] = None,
        year: Optional[str] = None,
        function_name=None,
        state_machine_name=None,
        dead_letter_queue_enabled=False,
        **kwargs,
    ):
        from aws_cdk import aws_events as eventbridge
        from aws_cdk import aws_events_targets as eventbridge_targets

        id = id or f"{self.func.__name__}_sched_{_sample()}"

        if expression is not None:
            schedule = eventbridge.Schedule.expression(expression)
        else:
            schedule = eventbridge.Schedule.cron(
                day=day,
                hour=hour,
                minute=minute,
                month=month,
                week_day=week_day,
                year=year,
            )

        rule = eventbridge.Rule(
            scope,
            id,
            schedule=schedule,
            **kwargs,
        )

        if not self.downstream:
            fn = self.aws_lambda(
                scope,
                function_name=function_name,
                dead_letter_queue_enabled=dead_letter_queue_enabled,
            )
            target = eventbridge_targets.LambdaFunction(handler=fn)
        else:
            state_machine = self.state_machine(
                scope,
                state_machine_name=state_machine_name,
            )
            target = eventbridge_targets.SfnStateMachine(machine=state_machine)

        rule.add_target(target)

        return rule


def enable_powertools(
    decorated=None,
    log_event=True,
    capture_response=True,
    capture_error=True,
    raise_on_empty_metrics=False,
    capture_cold_start_metric=True,
    default_dimentions=None,
    model=None,
    envelope=None,
):
    """
    AWS lambda powertools shortcut.

    Args:
        decorated: the function being decorated
        log_event: passed to aws_lambda_powertools.Logger
        capture_response: passed to aws_lambda_powertools.Tracer
        capture_error: passed to aws_lambda_powertools.Tracer
        raise_on_empty_metrics: passed to aws_lambda_powertools.Metrics
        capture_cold_start_metric: passed to aws_lambda_powertools.Metrics
        default_dimentions: passed to aws_lambda_powertools.Metrics
        model: passed to aws_lambda_powertools.utilities.parser.event_parser
        envelope: passed to aws_lambda_powertools.utilities.parser.event_parser

    For further descriptions, see https://awslabs.github.io/aws-lambda-powertools-python/latest/
    """

    from aws_lambda_powertools import Logger, Tracer, Metrics
    from aws_lambda_powertools.utilities.parser import event_parser

    def decorator(func):

        if isinstance(func, Compose):

            raise TypeError(
                f"@powertools decorator must be used BELOW the @compose decorator."
            )

        logger, tracer, metrics = (
            globals().get(x)
            for x in (
                "logger",
                "tracer",
                "metrics",
            )
        )

        if isinstance(logger, Logger):

            func = logger.inject_lambda_context(
                log_event=log_event,
            )(func)

        if isinstance(tracer, Tracer):

            func = tracer.capture_lambda_handler(
                capture_response=capture_response,
                capture_error=capture_error,
            )(func)

        if isinstance(metrics, Metrics):

            func = metrics.log_metrics(
                capture_cold_start_metric=capture_cold_start_metric,
                raise_on_empty_metrics=raise_on_empty_metrics,
                default_dimensions=default_dimentions,
            )(func)

        if model is not None:

            @functools.wraps(func)
            def mini_decorator(event, context):
                """
                Exists because event_parser expects the function it wraps to be named "handler".
                """

                result = event_parser(
                    handler=func,
                    model=model,
                    envelope=envelope,
                    event=event,
                    context=context,
                )

                return result

            func = mini_decorator

        return func

    if decorated is not None:
        return decorator(decorated)
    else:
        return decorator


compose = Compose
