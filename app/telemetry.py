"""
OpenTelemetry configuration and setup for the FastAPI application.
"""

import os
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor


def setup_opentelemetry():
    """
    Initialize OpenTelemetry tracing configuration.

    Returns:
        tracer: The configured tracer instance
    """
    # Initialize OpenTelemetry only if traces are enabled
    if os.getenv("OTEL_TRACES_EXPORTER", "none") != "none":
        # Initialize OpenTelemetry
        trace.set_tracer_provider(TracerProvider())
        tracer = trace.get_tracer(__name__)

        # Set up OTLP exporter with environment variable configuration
        otlp_endpoint = os.getenv(
            "OTEL_EXPORTER_OTLP_TRACES_ENDPOINT", "http://localhost:4317"
        )
        otlp_exporter = OTLPSpanExporter(endpoint=otlp_endpoint)
        span_processor = BatchSpanProcessor(otlp_exporter)
        trace.get_tracer_provider().add_span_processor(span_processor)
    else:
        # Create a no-op tracer when disabled
        tracer = trace.get_tracer(__name__)

    return tracer


def instrument_fastapi(app):
    """
    Instrument FastAPI with OpenTelemetry.

    Args:
        app: FastAPI application instance
    """
    # Automatically instrument FastAPI with OpenTelemetry only if traces are enabled
    if os.getenv("OTEL_TRACES_EXPORTER", "none") != "none":
        FastAPIInstrumentor.instrument_app(app)


def get_tracer():
    """
    Get the tracer instance for creating custom spans.

    Returns:
        tracer: The tracer instance
    """
    return trace.get_tracer(__name__)
