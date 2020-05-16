from folker.load.schemas import ActionSchema
from folker.module.grpc.schema import GrpcActionSchema

ActionSchema.type_schemas['GRPC'] = GrpcActionSchema
