from pydantic import BaseModel
from pydantic_settings import (
    BaseSettings,
    DotEnvSettingsSource,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    YamlConfigSettingsSource,
)


class QdrantConfig(BaseModel):
    url: str | None = None
    collection_name: str
    api_key: str | None = None


class PathSettings(BaseModel):
    yaml_path: str = None
    env_path: str = None


class GenerativeConfig(BaseModel):
    url: str
    model: str
    api_key: str | None = None


class EmbeddingConfig(BaseModel):
    model: str


class Model(BaseModel):
    embedding: EmbeddingConfig
    generative: GenerativeConfig


class Config(BaseSettings):
    qdrant: QdrantConfig
    model: Model
    path_settings: PathSettings = PathSettings()
    model_config = SettingsConfigDict(
        env_nested_delimiter="__",
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (
            init_settings,
            env_settings,
            DotEnvSettingsSource(settings_cls, env_file=cls.path_settings.env_path),
            YamlConfigSettingsSource(
                settings_cls, yaml_file=cls.path_settings.yaml_path
            ),
        )

    @classmethod
    def load(cls, path_settings: PathSettings) -> "Config":
        cls.path_settings = path_settings
        return cls()
