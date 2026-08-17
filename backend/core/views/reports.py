import json
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from core.models import Conversation, Message, ReportSummary
from core.serializers import ReportSummaryResponseSerializer
from core.services.ai_service import ai_service


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_report(request, conversation_id):
    try:
        conversation = Conversation.objects.get(id=conversation_id, user_id=request.user.id)
    except Conversation.DoesNotExist:
        return Response({'detail': 'Conversation not found'}, status=status.HTTP_404_NOT_FOUND)

    messages = list(Message.objects.filter(conversation_id=conversation_id).order_by('created_at'))
    if not messages:
        return Response({'detail': 'No messages in conversation'}, status=status.HTTP_400_BAD_REQUEST)

    conversation_messages = [{'role': m.role, 'content': m.content} for m in messages]
    summary_result = ai_service.generate_summary(conversation_messages)

    summary_data = summary_result.get('summary', summary_result)

    report = ReportSummary.objects.create(
        user_id=request.user.id,
        conversation_id=conversation_id,
        symptoms_mentioned=json.dumps(summary_data.get('symptoms_mentioned', [])),
        duration=summary_data.get('duration', ''),
        key_info=summary_data.get('key_information', ''),
        questions_discussed=json.dumps(summary_data.get('questions_discussed', [])),
        guidance=summary_data.get('guidance_provided', ''),
        warning_signs=json.dumps(summary_data.get('warning_signs', [])),
        next_steps=json.dumps(summary_data.get('next_steps', [])),
    )
    return Response(ReportSummaryResponseSerializer(report).data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_reports(request):
    reports = ReportSummary.objects.filter(user_id=request.user.id).order_by('-created_at')
    return Response(ReportSummaryResponseSerializer(reports, many=True).data)


@api_view(['GET', 'DELETE'])
@permission_classes([IsAuthenticated])
def report_detail(request, report_id):
    try:
        report = ReportSummary.objects.get(id=report_id, user_id=request.user.id)
    except ReportSummary.DoesNotExist:
        return Response({'detail': 'Report not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        report.delete()
        return Response({'message': 'Report deleted'})

    return Response(ReportSummaryResponseSerializer(report).data)
