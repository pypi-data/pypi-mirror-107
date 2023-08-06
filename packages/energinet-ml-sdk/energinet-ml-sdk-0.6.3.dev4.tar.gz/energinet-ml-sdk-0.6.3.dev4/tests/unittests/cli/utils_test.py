import os
import click
import pytest
import tempfile
from click.testing import CliRunner
from unittest.mock import patch, Mock

from energinetml.core.project import Project
from energinetml.core.model import (
    Model,
    ModelImportError,
    ModelNotClassError,
    ModelNotInheritModel,
)
from energinetml.cli.utils import (
    discover_project,
    discover_model,
)


PROJECT_NAME = 'NAME'
PROJECT_SUBSCRIPTION_ID = 'SUBSCRIPTION-ID'
PROJECT_RESOURCE_GROUP = 'RESOURCE-GROUP'
PROJECT_WORKSPACE_NAME = 'WORKSPACE-NAME'

MODEL_NAME = 'NAME'
MODEL_EXPERIMENT = 'EXPERIMENT'
MODEL_COMPUTE_TARGET = 'COMPUTE-TARGET'
MODEL_VM_SIZE = 'VM-SIZE'
MODEL_DATASETS = ['iris', 'hades:2']
MODEL_FEATURES = ['feature1', 'feature2']
MODEL_PARAMETERS = {'param1': 'value1', 'param2': 'value2'}


# -- discover_project() Tests ------------------------------------------------


@click.command()
@discover_project()
def discover_project_testable(project):
    pass


@patch('energinetml.cli.utils.Project.from_directory')
def test__discover_project__project_exists__should_exit_with_status_ok(from_directory_mock):  # noqa: E501
    runner = CliRunner()

    # Act
    result = runner.invoke(discover_project_testable, ['--path', 'mock-path'])

    # Assert
    assert result.exit_code == 0


@patch('energinetml.cli.utils.Project.from_directory')
def test__discover_project__project_does_not_exist__should_exit_with_error(from_directory_mock):  # noqa: E501
    with tempfile.TemporaryDirectory() as path:
        from_directory_mock.side_effect = Project.NotFound

        runner = CliRunner()

        # Act
        result = runner.invoke(discover_project_testable, ['--path', path])

        # Assert
        assert result.exit_code == 1

        from_directory_mock.assert_called_once_with(path)


# -- discover_model() Tests --------------------------------------------------


@click.command()
@discover_model()
def discover_model_testable(model):
    """
    Empty function to allow invoking the decorator.
    """
    pass


@patch('energinetml.cli.utils.os.path.isfile')
def test__discover_model__model_file_does_not_exists__should_exit_with_error(isfile_mock):  # noqa: E501
    """
    :param Mock isfile_mock:
    """
    with tempfile.TemporaryDirectory() as path:
        isfile_mock.return_value = False

        runner = CliRunner()

        # Act
        result = runner.invoke(discover_model_testable, ['--path', path])

        # Assert
        assert result.exit_code == 1

        isfile_mock.assert_called_once_with(
            os.path.join(path, Model.SCRIPT_FILE_NAME))


@patch('energinetml.cli.utils.os.path.isfile')
@patch('energinetml.cli.utils.import_model_class')
@pytest.mark.parametrize('exception', (
        ModelImportError,
        ModelNotClassError,
        ModelNotInheritModel,
))
def test__discover_model__import_model_class_raises_exception__should_exit_with_error(
        import_model_class_mock, isfile_mock, exception):
    """
    :param Mock import_model_class_mock:
    :param Mock isfile_mock:
    :param Exception exception:
    """
    with tempfile.TemporaryDirectory() as path:
        isfile_mock.return_value = True
        import_model_class_mock.side_effect = exception

        runner = CliRunner()

        # Act
        result = runner.invoke(discover_model_testable, ['--path', path])

        # Assert
        assert result.exit_code == 1

        isfile_mock.assert_called_once_with(
            os.path.join(path, Model.SCRIPT_FILE_NAME))
        import_model_class_mock.assert_called_once_with(
            os.path.join(path, Model.SCRIPT_FILE_NAME))


@patch('energinetml.cli.utils.os.path.isfile')
@patch('energinetml.cli.utils.import_model_class')
def test__discover_model__model_not_found_in_directory__should_exit_with_error(
        import_model_class_mock, isfile_mock):
    """
    :param Mock import_model_class_mock:
    :param Mock isfile_mock:
    """
    with tempfile.TemporaryDirectory() as path:
        model_class = Mock()
        model_class.from_directory.side_effect = Model.NotFound
        isfile_mock.return_value = True
        import_model_class_mock.return_value = model_class

        runner = CliRunner()

        # Act
        result = runner.invoke(discover_model_testable, ['--path', path])

        # Assert
        assert result.exit_code == 1

        isfile_mock.assert_called_once_with(
            os.path.join(path, Model.SCRIPT_FILE_NAME))
        import_model_class_mock.assert_called_once_with(
            os.path.join(path, Model.SCRIPT_FILE_NAME))
